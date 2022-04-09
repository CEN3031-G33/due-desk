# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : desk
# Abstract : 
#   The desk is in charge of loading/storing the resources on its desk, and
#   managing the available tasks. 
# ------------------------------------------------------------------------------
import unittest
import json, os
from .tasklistgui import TasklistGui
from .resourcepoolgui import *
from PyQt5.QtWidgets import *

class Desk: 
    def __init__(self, filepath: str, root: QMainWindow):
        '''Creates a `Desk` instance.'''
        self._root = root
        self._file = filepath
        self._tlg = TasklistGui(self._root, [])
        self._plg = Pool(self._root, [])
        self._ilg = Inventory(self._root, [], self._plg)
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
            # hand off data to tasklist gui
            self._tlg.load(data)
            self._tlg.glue_to_gui()
            # :todo: hand off data to inventory gui
            self._ilg.load({})
            self._ilg.glue_to_gui()
        pass


    def save_to_file(self) -> None:
        '''Saves the desk's current state to the file.'''
        # :todo:
        data = {}
        # self._tlg.save()
        self._ilg.save()
        self._plg.save()

        # write contents to file
        # json.dump(data, fp)
        pass


    def set_file(self, f: str) -> None:
        self._file = f


    def get_file(self) -> str:
        return self._file
    pass


class TestDesk(unittest.TestCase):
    def test_new(self):
        #d = Desk(None, "./tests/data.json")
        #d.load_from_file()
        pass
    pass