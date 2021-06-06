"""
rell will be the linker between the query(pyke.py)
and the api(blitz)/scrapper(zoe)
"""

from pyke import Pyke, accountTypes
import blitz
import veigar
import time

cache = veigar.Veigar()


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
    assert type(query) is Pyke
    ret = templateDict()
    interpreted = ""
    if "matches" in query.selection:
        interpreted += query.selection
        for account in query.accounts:
            if account[0] is accountTypes.name:
                pass

    ret["queryTimestamp"] = time.time()
    ret["query"] = interpreted
    ret["settings"] = Pyke.settings()
