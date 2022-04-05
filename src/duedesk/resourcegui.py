# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : ResourceGui
# Abstract : 
#   A desk item is composed of gui related materials such as `Button` and
#   business logic-related materials for `Resource`. It couples them together.
# ------------------------------------------------------------------------------
import unittest
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from .resource import Resource

class ResourceGui(QWidget):
    def __init__(self, root: QMainWindow):
        '''Creates a `ResourceGui` instance.'''
        super(QWidget, self).__init__(root)
        self._button = QPushButton(root)
        self._filepath = "./resources/pc.png"
        self._image = QIcon(self._filepath)
        self._button.setIcon(self._image)
        self._button.setIconSize(QSize(64, 64))
        self._button.clicked.connect(self.bring_to_desk)
        self._resource = Resource(self._filepath, (0, 0), False, False, 0)
        pass


    def glue_to_gui(self, layout: QFormLayout):
        if self._resource.is_inscene() == True:
            self._button.clicked.connect(self.move_around_desk)
            self._button.move(self._resource.get_location()[0], self._resource.get_location()[1])
        else:
            self._button.clicked.connect(self.bring_to_desk)
        layout.addWidget(self._button)
        pass


    def load(self, data: dict) -> None:
        '''Loads `Resource` attributes from a dictionary into existing instance.'''
        self._resource = Resource.from_dict(data)
        self._image = QIcon(self._resource.get_filepath())
        self._button.setIcon(self._image)
        pass


    # method bound to clicking the image for `ResourceGui` object in context of inventory
    def bring_to_desk(self):
        print('info: bringing in inventory item to the desk')
        # :todo: make a copy/new button onto desk (maybe handled by upper-level glue for resource pool)
        pass


    def show(self):
        self._button.show()


    def get_resource(self) -> Resource:
        return self._resource

    # method bound to clicking the image for `ResourceGui` object in context of desk
    def move_around_desk(self):
        print('info: moving item around the desk')
        pass
    pass


class TestResourceGui(unittest.TestCase):
    pass