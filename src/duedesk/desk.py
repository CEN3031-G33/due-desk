# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : desk
# Abstract : 
#   The desk is in charge of loading/storing the resources on its desk, and
#   managing the available tasks. 
# ------------------------------------------------------------------------------
import unittest
import json, os
from .tasklist import Tasklist

class Desk: 
    def __init__(self, filepath: str):
        '''Creates a `Desk` instance.'''
        self._file = filepath
        # :note: instead of storing actual tasks, need to store the glue items for
        #   smooth interface between business logic and gui
        self._tl = Tasklist([])
        pass

    
    def load_from_file(self) -> None:
        '''Modifies the desk instance with data from the file.'''
        # create file if doesn't exist
        if os.path.isfile(self.get_file()) == False:
            with open(self.get_file(), 'w') as fp:
                json.dump({}, fp)
        # read contents from file
        with open(self.get_file(), 'r') as fp:
            data = json.load(fp)
            print(data)
            # :todo: parse data in data structure accordingly
        pass


    def save_to_file(self) -> None:
        '''Saves the desk's current state to the file.'''
        # :todo:
        pass


    def set_file(self, f: str) -> None:
        self._file = f


    def get_file(self) -> str:
        return self._file
    pass


class TestDesk(unittest.TestCase):
    def test_new(self):
        d = Desk("./tests/data.json")
        d.load_from_file()
        pass
    pass