"""
veigar will be the cage, to save to a database. It will use RAM info if a
database is not specified in the veigar object creation.
"""
# TODO: make a way to force for a new query
import sqllite3 as sql
from sqllite3 import ProgrammingError as sqlError
from sqllite3 import OperationalError as transitionError
import os
from enum import Enum, auto
from blitz import Account


class accountTypes(Enum):
    # TODO do the rest and change the name
    sumid = auto()
    name = auto()
    ppuid = auto()
    accountId = auto()


class Veigar:
    def __init__(self, name="main", path=None):
        # TODO
        """
        if the path is False it will use ram

        """
        if path is False:
            path = ":memory:"
        elif path is None:
            path = os.getenv("APPDATA") + "\\.veigar"
        if path.endswith(".db"):
            self.path = path
        else:
            self.path = path + "\\" + name + ".db"

    def executeQuery(query):
        # TODO
        pass

    def getAccount(self, accountIdentifier, acctype, maxTime=864000):
        # TODO
        # if it doesn't find an account saved it returns null
        # maxTime says that if the saved is older than that then it returns null
        # if maxTime is none it will always return NoNE
        assert type(acctype) is accountTypes
        return None

    def saveAccount(self, account):
        # TODO
        assert type(account) is Account
