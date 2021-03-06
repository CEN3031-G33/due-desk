# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : resourcepoolgui
# Abstract : 
#   Resourcepoolgui's are used to store resources in two areas: desk table 
#   (pool) and the desk inventory (inventory). Manages Resourcegui objects.
# -----------------------------------------------------------------------------
from .resourcegui import ResourceGui
from typing import List
from PyQt5.QtWidgets import *

class Pool(QWidget):
    '''Maintains items currently on the desk table.'''
    def __init__(self, root: QMainWindow, inner: List[ResourceGui]):
        super(QWidget, self).__init__(root)
        self._root = root
        self._inner = inner
        pass


    def glue_to_gui(self):
        # place all ResourceGui's in the window
        for rsc in self._inner:
            rsc.glue_to_gui(None)
        pass


    def add(self, rg: ResourceGui) -> None:
        '''Adds a new resource to the desk table.'''
        self._inner += [rg]
        pass


    def remove(self, rg: ResourceGui) -> None:
        '''Removes a resource from the desk table using full_eq comparison.'''
        for item in self._inner:
            if rg.get_resource().full_eq(item.get_resource()) == True:
                self._inner.remove(item)
                break
        pass


    def load(self, data: dict):
        rsc_pool_list = []
        for v in data.values():
            rg = ResourceGui(self._root, self)
            rg.load(v, True)
            rsc_pool_list += [rg]

        self._inner = rsc_pool_list
        pass


    def save(self) -> dict:
        print('info: saving pool...')
        data = {}
        for (i,rg) in enumerate(self._inner):
            data[str(i)] = rg.save()
        return data
    pass


class Inventory(QWidget):
    '''Maintains items available for the desk table.'''
    def __init__(self, root: QMainWindow, inner: List[ResourceGui], pool: Pool):
        super(QWidget, self).__init__(root)
        self._root = root
        self._inner = inner
        self._pool = pool

        screen = QApplication.primaryScreen()
        self._form_layout = QFormLayout()

        self.resize(int(screen.size().width() * 0.8), int(screen.size().height() * 0.2))
        self.move(0, int(screen.size().height() * 0.8))

        self._hbox = QHBoxLayout()
        self._group_box = QGroupBox("")
        self._group_box.setStyleSheet("text-align: center; font-size: 10px; font-family: Menlo;")
        
        scroll = QScrollArea()
        scroll.setWidget(self._group_box)
        scroll.setWidgetResizable(True)

        self._layout = QVBoxLayout()
        self._layout.addWidget(scroll)
        pass


    def glue_to_gui(self):
        # add inventory items to the gui
        for rg in self._inner:
            rg.glue_to_gui(self._hbox)

        self._group_box.setLayout(self._hbox)
        title = "Inventory (" + str(len(self._inner)) + ")"
        self._group_box.setTitle(title)

        self.setLayout(self._layout)
        self.show()
        pass


    def load(self, data: dict):
        # set to false for inscene
        rsc_inv_list = []
        # :todo: handle dups & doesn't care positions
        for v in data.values():
            rg = ResourceGui(self._root, self._pool) # pool is a list wrapper
            rg.load(v, False)
            rg.get_resource().set_inscene(False)
            rsc_inv_list += [rg]

        self._inner = rsc_inv_list
        pass


    def save(self) -> dict:
        '''Saves the Resourcegui's as dictionaries from inventory.'''
        data = dict()
        print('info: saving inventory...')
        for (i,rg) in enumerate(self._inner):
            data[str(i)] = rg.save()
        return data
    pass