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
            for (key, val) in data.items():
                # hand off data to tasklist gui
                if key == 'tasks':
                    self._tlg.load(val)
                # hand off data to inventory gui
                elif key == 'inventory':
                    self._ilg.load(val)
                # hand off data to desk gui
                elif key == 'desk':
                    self._plg.load(val)
            pass              
        self._tlg.glue_to_gui()
        self._ilg.glue_to_gui()
        self._plg.glue_to_gui()
        pass


    def save_to_file(self) -> None:
        '''Saves the desk's current state to the file.'''
        data = {}
        data['inventory'] = self._ilg.save()
        data['desk'] = self._plg.save()
        data['tasks'] = self._tlg.save()
        with open(self._file, 'w') as fp:
            json.dump(data, fp, indent=1)
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