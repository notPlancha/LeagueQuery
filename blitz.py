from riotwatcher import ApiError, LolWatcher
from loguru import logger as log
import time
from veigar import accountTypes
from enum import Enum, auto

# Eventually change to matchesV5 but since the filtering options is basically
# none, ¯\_(ツ)_/¯
# TODO change every type to isintance
league_get = LolWatcher("RGAPI-97b317ef-97ae-48ef-8e05-b216ab8ac4a9")
endpoints = {
    "matchv4": league_get.match,
    "matches": league_get.match,
    "summoner": league_get.summoner,
    "account": league_get.summoner,
    "ddragon": league_get.data_dragon,
    "patches": None,  # https://ddragon.leagueoflegends.com/api/versions.json
    "current_version": league_get.data_dragon.versions_for_region,
    "matchlist": league_get.match.matchlist_by_account,
    "match": league_get.match.by_id,
}


class queueTypes(Enum):
    # http://static.developer.riotgames.com/docs/lol/queues.json
    HexakillAbyss = 75
    # Urf = 76
    OneForAllMirrored = 78
    UrfAi = 83
    HexakillTreeline = 98
    ButchersBridge = 100
    Nemesis = 310
    BlackMarket = 313
    NotDominion = 317
    AllRandomRift = 325
    Draft = 400
    SoloDuo = 420
    Blind = 430
    Flex = 440
    Aram = 450
    BloodHunt = 600
    DarkStar = 610
    Clash = 700
    AiTreelineBegginer = 820
    AiIntro = 830
    AiBegginer = 840
    AiInter = 850
    Urf = 900
    Ascension = 910
    PoroKing = 920
    NexusSiege = 940
    DoomBotsVoting = 950
    DoomBotsStandart = 960
    StarGuardianNormal = 980
    PROJECT = 1000
    SnowArurf = 1010
    OneForAll = 1020
    OdysseyIntro = 1030
    OdysseyCadet = 1040
    OdysseyCrewmember = 1050
    OdysseyCaptain = 1060
    OdysseyOnslaught = 1070
    TFT = 1090
    RankedTFT = 1100
    TutorialTFT = 1110
    TestTFT = 1111
    NexusBlitz = 1300
    Tutorial1 = 2000
    Tutorial2 = 2010
    Tutorial3 = 2030


def current_version(region):
    return endpoints["current_version"](region)["v"]


def getChampionFromKey(key):
    championsDict = endpoints["ddragon"].champions(current_version("euw"))["data"]
    for i in championsDict:
        if key == championsDict[i]["key"]:
            return championsDict[i]["name"]
    raise KeyError()


def getKeyFromChampion(championName):
    if championName.lower() == "nunu":
        return "20"
    championName = championName.capitalize()
    if championName == "Nunu":
        return "20"
    championsDict = endpoints["ddragon"].champions(current_version())["data"]
    return championsDict[championName]


class Account:
    def __init__(self, region, account):
        assert type(account) is dict
        # TODO change names to dict only
        self.name = account["name"]
        self.region = region
        self.SummonerId = account["id"]
        self.AccountId = account["accountId"]
        self.GlobalId = account["puuid"]
        self.profileIcon_id = account["profileIconId"]
        self.summonerLevel = account["summonerLevel"]
        # self.matchHistory = []

    def getMatchHistory(
        self,
        start_date=None,
        end_date=None,
        queueIds=None,
        index=(0, 0 + 100),
        champions=None,
    ):
        assert (
            all([isinstance(i, int) for i in index]) and 0 < index[1] - index[0] <= 100
        )
        if champions is not None:
            if type(champions) is int:
                champions = [champions]
            elif type(champions) is str:
                champions = [getKeyFromChampion(champions)]
            else:
                assert type(champions) is list
                if type(champions[0]) is str:
                    champions = [getKeyFromChampion(i) for i in champions]
        if start_date is not None:
            if type(start_date) is time.struct_time:
                start_date = int(time.mktime(start_date))
            elif type(start_date) is float:
                start_date = int(start_date)
            else:
                assert type(start_date) is int
        if end_date is not None:
            if type(end_date) is time.struct_time:
                end_date = int(time.mktime(end_date))
            elif type(end_date) is float:
                end_date = int(end_date)
            else:
                assert type(end_date) is int
        assert end_date > start_date
        if queueIds is not None:
            if type(queueIds) is queueTypes:
                queueIds = [queueIds.value]
            else:
                assert type(queueIds) is list
                queueIds = [id.value for id in queueIds]

        try:
            matches = endpoints["matchlist"](
                self.region,
                self.AccountId,
                queue=queueIds,
                begin_time=start_date,
                end_time=end_date,
                begin_index=index[0],
                end_index=index[1],
            )
        except ApiError as err:
            raise ApiError("error: " + str(err.response.status_code))
        return matches["matches"]

    @staticmethod
    def get(identifier, acctype, region):
        assert type(acctype) is accountTypes
        assert identifier is not None and region is not None
        if region == "euw":
            region = "euw1"
        else:
            region = region
        if acctype == accountTypes.name:
            endpoint = endpoints["account"].by_name
        elif acctype == accountTypes.accountId:
            endpoint = endpoints["account"].by_account
        elif acctype == accountTypes.ppuid:
            endpoint = endpoints["account"].by_puuid
        elif acctype == accountTypes.sumid:
            endpoint = endpoints["account"].by_id
        else:
            raise ValueError("not an accType")
        try:
            account = endpoint(region, identifier)
        except ApiError as err:
            raise Exception("error: " + str(err.response.status_code))
        return Account(region, account)


class Player:
    # this is for the matches
    def __init__(self, account, championId):
        assert type(account) is Account
        self.account = account
        self.championId = championId


class Team:
    def __init__(self, id, players, bansIds):
        assert type(players) is list
        assert all(type(i) is Player for i in players)
        assert type(bansIds) is list
        # TODO verify if this is the case
        if id == "100" or id == "left":
            self.id = "left"
        elif id == "200" or id == "right":
            self.id = "right"
        else:
            raise ValueError("teamId neither")
        self.players = players
        self.bansIds = bansIds


class Match:
    def __init__(self, matchId, AccountFrom=None, get=False):
        self.matchId = matchId
        self.got = False
        if get:
            self.get()
        if AccountFrom is not None:
            self.userRequested = self.getPlayer(Account)
        else:
            self.userRequested = None

    # TODO
    def get(self):
        self.got = True
        self.teamLeft = None
        self.teamRight = None

    def getPlayer(self, accountName):
        if type(accountName) is Account:
            accountName = accountName.name
        pass

    def getTimeLine(self):
        pass

    @staticmethod
    def getById(id):
        return Match(id, AccountFrom=None, get=True)


if __name__ == "__main__":
    # print(len(Account.get("notPlancha", "euw").getPMatchHistory()["matches"]))
    print(current_version("euw"))
    print(getChampionFromKey("34"))
