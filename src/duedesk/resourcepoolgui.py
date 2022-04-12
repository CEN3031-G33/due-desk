from duedesk.resourcepool import Resourcepool
from .resourcegui import ResourceGui
from typing import List
from PyQt5.QtWidgets import *

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
            # assumes all resources are `inscene`
            rsc.glue_to_gui(None)
        pass


    def add(self, rg: ResourceGui) -> None:
        '''Adds a new resource to the desk table.'''
        self._inner += [rg]
        pass


    def load(self, data: dict):
        rsc_pool_list = []
        for v in data.values():
            rg = ResourceGui(self._root, self)
            rg.load(v)
            rg.get_resource().set_inscene(True)
            rsc_pool_list += [rg]

        self._inner = rsc_pool_list
        pass


    def save(self) -> dict:
        data = {}
        print('saving pool')
        for (i,rg) in enumerate(self._inner):
            data[str(i)] = rg.save()
        return data
    pass


# items available to put on the desk
class Inventory(QWidget):
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


    # handle dups & doesn't care positions
    def load(self, data: dict):
        # set to false for inscene
        rsc_inv_list = []
        for v in data.values():
            rg = ResourceGui(self._root, self._pool) # pool is a list wrapper
            rg.load(v)
            rg.get_resource().set_inscene(False)
            rsc_inv_list += [rg]

        self._inner = rsc_inv_list
        pass

    # save the resourcegui's as dictionaries from inventory
    def save(self) -> dict:
        data = dict()
        print('saving inventory')
        for (i,rg) in enumerate(self._inner):
            data[str(i)] = rg.save()
        return data

    pass

