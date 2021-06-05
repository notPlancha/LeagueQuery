"""
pyke will be the executer, reader of the query
and communication with the linker (rell)
"""
# returns a dict


def templateDict():
    return {
        "queryTimestamp": None,
        "query": None,
        # "dataFrom":[]#cached, [websites] TODO
        "data": {},
    }


def execute(query):
    print(query)


class Pyke:
    def __init__(self):
        self.selection = "games"
        self.account = ""
