from riotwatcher import ApiError, LolWatcher

# Eventually change to matchesV5 but since the filtering options is basically
# null, ¯\_(ツ)_/¯

league_get = LolWatcher("RGAPI-5b839b7a-75fa-41a2-987e-95ca8cb3cc9a")
endpoints = {
    "matchv4": league_get.match,
    "matches": league_get.match,
    "summoner": league_get.summoner,
    "account": league_get.summoner,
    "ddragon": league_get.data_dragon,
    "patches": None,  # https://ddragon.leagueoflegends.com/api/versions.json
    "current_version": league_get.data_dragon.versions_for_region,
    "matchlist": league_get.match.matchlist_by_account,
}


def current_version(region):
    return endpoints["current_version"](region)["v"]


def getChampionFromKey(key):
    championsDict = endpoints["ddragon"].champions(current_version())["data"]
    for i in championsDict:
        if key == i["key"]:
            return i["name"]
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
        self.name = name
        self.region = region
        self.SummonerId = account["id"]
        self.AccountId = account["accountId"]
        self.GlobalId = account["puuid"]
        self.profileIcon_id = account["profileIconId"]
        self.summonerLevel = account["summonerLevel"]
        self.matchHistory = []

    def getMatchHistory(
        self,
    ):
        try:
            matches = endpoints["matchlist"](
                self.region,
                self.AccountId,
            )
        except ApiError as err:
            raise Exception("error: " + str(err.response.status_code))
        matches["matches"]

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
    def __init__(self):
        pass


class Match:
    def __init__(self):
        pass


if __name__ == "__main__":
    # print(len(Account.get("notPlancha", "euw").getPMatchHistory()["matches"]))
    print(current_version("euw"))
    print(endpoints["ddragon"].champions("11.11.1"))
