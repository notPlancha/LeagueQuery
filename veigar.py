"""
veigar will be the cage, to save to a database. It will use RAM info if a
database is not specified in the veigar object creation.
# TODO: make a way to force for a new query
"""
import sqllite3 as sql
from sqllite3 import ProgrammingError as sqlError
from sqllite3 import OperationalError as transitionError
import os


class Veigar:
    def __init__(self, name, path=None):
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
