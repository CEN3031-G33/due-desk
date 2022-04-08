from .resourcegui import ResourceGui
from typing import List
from PyQt5.QtWidgets import *

# items available to put on the desk
class Inventory(QWidget):
    def __init__(self, root: QMainWindow, inner: List[ResourceGui]):
        super(QWidget, self).__init__(root)
        self._root = root
        self._inner = inner

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
        for _ in range(0,50):
            self._inner += [ResourceGui(self._root, self._inner).glue_to_gui(self._hbox)]

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
            rg = ResourceGui(self._root)
            rg.load(v)
            rg.get_resource().set_inscene(False)
            rsc_inv_list += [rg]

        self._inner = rsc_inv_list
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
        rsc_pool_list = []
        for v in data.values():
            rg = ResourceGui(self._root)
            rg.load(v)
            rg.get_resource().set_inscene(True)
            rsc_pool_list += [rg]

        self._inner = rsc_pool_list
        pass
    pass