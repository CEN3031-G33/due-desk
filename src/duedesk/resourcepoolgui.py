from .resourcegui import ResourceGui
from typing import List
from PyQt5.QtWidgets import *

# items available to put on the desk
class Inventory:
    def __init__(self):
        pass

    # handle dups & doesn't care positions
    def load(self, data: dict):
        # set to false for inscene
        pass
    pass


# everything on the desk
class Pool(QWidget):
    def __init__(self, root: QMainWindow, inner: List[ResourceGui]):
        super(QWidget, self).__init__(root)
        self._root = root
        self._inner = inner
        pass


    def glue_to_gui(self):
        # place all ResourceGui's in the window
        for rsc in self._inner:
            #rsc.glue_to_gui()
            rsc.show()
        pass


    def load(self, data: dict):
        rsc_list = []
        for v in data.values():
            rg = ResourceGui(self._root)
            rg.load(v)
            rg.get_resource().set_inscene(True)
            rsc_list += [rg]

        self._inner = rsc_list
        pass
    pass