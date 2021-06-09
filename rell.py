"""
rell will be the linker between the query(pyke.py)
and the api(blitz)/scrapper(zoe)
and the veigar
"""

from pyke import Pyke, accountTypes, Matches
import blitz
import veigar
import time


def templateDict():
    return {
        "queryTimestamp": None,
        "query": None,  # Interpreted
        "requests": 0,  # number of requests to the api
        "limit": False,  # reached the limit of api requests api, either
        # "dataFrom":[]#cached, [websites] TODO
        "settings": None,
        "data": {},
    }


def get(query):
    # TODO make the interpreted
    assert isinstance(query, Pyke)
    cache = query.veigar
    if isinstance(query, Matches):
        ret = templateDict()
        interpreted = ""  # TODO do interpreted later
        accounts = []
        for account in query.accounts:
            accountObj = None
            if account[0] in [accountTypes.name]:
                if query.useCached:
                    accountObj = cache.getAccount(account[1], [account[0]])
                    if accountObj is not None:
                        account = True
                if account is not True:
                    accountObj = blitz.Account.get()  # make something if not found TODO
                    ret["requests"] += 1
                    accounts.append(accountObj)
                    if query.cache:
                        cache.saveAccount(accountObj)
        if "includes" in query.filters:
            includesFilters = query.filters["includes"]
            if "enemies" in includesFilters:
                if type(includesFilters["enemies"]) in [str, int]:
                    includesFilters = [includesFilters["enemies"]]
                else:
                    assert includesFilters["enemies"] is list
                    includesFilters = includesFilters["enemies"]
        else:
            includesFilters = None
        if "date" in query.filters:
            # Complete this and other filters TODO
            # for this maybe make a loop? idk
            # Make multiple dates too TODO
            dateFilters = query.filters["date"]
            if "between" in dateFilters:
                pass
        else:
            dateFilters = None
        if query.maximizeQuery:
            # extend query's date or smth idk TODO, right now this is the main getter but the maximaze query will be done later
            pass
        else:
            pass
        ret["queryTimestamp"] = time.time()
        ret["query"] = interpreted
        ret["settings"] = Pyke.settings()
        return ret
    else:
        # TODO implement other than matcghes
        raise NotImplementedError()
