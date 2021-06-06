"""
rell will be the linker between the query(pyke.py)
and the api(blitz)/scrapper(zoe)
"""

from pyke import Pyke, accountTypes
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
    cache = query.veigar
    assert type(query) is Pyke
    ret = templateDict()
    interpreted = ""
    if "matches" in query.selection:
        interpreted += query.selection
        for account in query.accounts:
            accountObj = None
            if account[0] in [accountTypes.name]:
                if query.useCached:
                    accountObj = cache.getAccount(account[1], [account[0]])
                    if accountObj is not None:
                        account = True
                if account is not True:
                    accountObj = blitz.Account.get()
                    ret["requests"] += 1

    ret["queryTimestamp"] = time.time()
    ret["query"] = interpreted
    ret["settings"] = Pyke.settings()
