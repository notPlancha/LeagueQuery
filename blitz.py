from riotwatcher import ApiError, LolWatcher
from loguru import logger as log
import time

# Eventually change to matchesV5 but since the filtering options is basically
# null, ¯\_(ツ)_/¯

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
    def __init__(self, name, region, account):
        assert type(account) is dict
        self.name = name
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
    ):
        if start_date is None:
            start_date = int(time.time())
        try:
            matches = endpoints["matchlist"](
                self.region,
                self.AccountId,
            )
        except ApiError as err:
            raise Exception("error: " + str(err.response.status_code))
        return matches["matches"]

    @staticmethod
    def get(name, region):
        assert name is not None and region is not None
        if region == "euw":
            region = "euw1"
        else:
            region = region
        try:
            account = endpoints["account"].by_name(region, name)
        except ApiError as err:
            raise Exception("error: " + str(err.response.status_code))
        return Account(name, region, account)


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
