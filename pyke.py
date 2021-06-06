"""
pyke will be the executer and parser of the query
and communication with the linker (rell)
"""
# * is equal to matches, unless specified in the settings
# if no start/end date is specified it will only bringmatches from last week
# + chached, unless settings changed
# returns a dict

import rell
import veigar
from rell.veigar import accountTypes
from enum import Enum, auto
import warnings

apiKey = None


class apiKeyType(Enum):
    Personal = auto()
    # TODO add others


apitype = apiKeyType.Personal


def execute(query):
    return Pyke(query).execute()


class Pyke:
    def __init__(self, query, **kwargs):
        # here is the query parser TODO
        self.selection = ["matches"]  # TODO make options enum
        self.accounts = [(accountTypes.name, "notPlancha")]

        # default settings
        self.api = apiKey
        self.waitUntilFullRequest = False
        self.apiType = apiKeyType
        self.allismatches = True
        self.useCached = True
        self.cache = True
        self.veigar = veigar.Veigar()
        if len(kwargs.values()) > 0:
            self.options(kwargs)

    def execute(self):
        return rell.get(self)

    def options(self, **kwargs):
        if "api" in kwargs:
            self.api = kwargs.get("api")
        if "apiKeyType" in kwargs:
            self.apiType = kwargs.get("apiKeyType")
        if "allismatches" in kwargs:
            if type(kwargs.get("allismatches")) is bool:
                self.allismatches = kwargs.get("allismatches")
            else:
                warnings.warn("allismatches option must be bool, ignored option")
        # add cache and cached TODO

    def getOptions(self):
        return {}
