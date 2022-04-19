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
    def __init__(self, root: QMainWindow, pool): # pool: Pool
        '''Creates a `ResourceGui` instance.'''
        super(QWidget, self).__init__(root)
        self._button = QPushButton(self)
        self._button.setIconSize(QSize(64, 64))
        self._filepath = "./resources/util/unknown.png"
        self._image = QIcon(self._filepath)
        self._button.setIcon(self._image)
        self._button.resize(QSize(64, 64))
        self._resource = Resource(self._filepath, (0, 0), False, False, 0)
        self._root = root
        self._pool = pool
        pass


    def glue_to_gui(self, layout: QFormLayout):
        '''Attaches the PyQt5 gui elements to the layout. If `layout` is `None`, the resource is not added to QFormLayout.'''
        if layout == None:
            self._button.clicked.connect(self.move_around_desk) # :todo: maybe remove line?
            self._button.move(int(self._resource.get_location()[0]), int(self._resource.get_location()[1]))
        else:
            self._button.clicked.connect(self.bring_to_desk)
            layout.addWidget(self._button)
        self._button.resize(QSize(64, 64))
        self._button.show()
        pass

    
    def update_icon(self):
        '''Verifies the resource's filepath is valid before trying to display. If its invalid, 
        the icon is set to an '?' image. Updates the `self._button`'s icon.'''
        # verify the filepath is valid
        if self.get_resource().is_filepath_valid() == True:
            self._image = QIcon(self.get_resource().get_filepath())
        else:
            self._image = QIcon('./resources/util/unknown.png')
        self._button.setIcon(self._image)
        pass


    def load(self, data: dict, draggable: bool) -> None:
        '''Loads `Resource` attributes from a dictionary into existing instance.'''
        self._resource = Resource.from_dict(data)
        # use draggable button (for desk table)
        if draggable:
            self._button = DragNDropButton(self._root, self)
        self.update_icon()
        self._button.setIcon(self._image)
        pass


    # method bound to clicking the image for `ResourceGui` object in context of inventory
    def bring_to_desk(self):
        if (self._resource.get_cost() <= self._root.getCredits()):
            if self.get_resource().is_filepath_valid() == False:
                print('error: cannot bring item to desk due to invalid filepath ', self.get_resource().get_filepath())
                return
            print('info: bringing in inventory item to the desk')
            # :todo: make a copy/new button onto desk (maybe handled by upper-level glue for resource pool)
            rg = ResourceGui(self._root, self._pool)
            rg._resource = self.get_resource()
            #rg.get_resource().set_inscene(True)
            rg._button = DragNDropButton(self._root, self)
            rg.update_icon()
            rg._button.move(100,260)
            rg._button.show()

            self._root.updateDeskCredits(-1 * self._resource.get_cost())
            self._pool.add(rg)
        else:
            print("info: insufficient credits!")
        pass


    def get_resource(self) -> Resource:
        return self._resource


    # method bound to clicking the image for `ResourceGui` object in context of desk
    def move_around_desk(self):
        print('info: moving item around the desk')
        pass
    

    def save(self) -> dict:
        '''Serializes the resource object. This method updates the resource's location before
        serialization.'''
        # extract x and y from button and put into resource
        self.get_resource().set_location((self._button.x(),self._button.y()))
        # print(self.get_resource().get_location())
        return self.get_resource().to_dict()
    pass


class DragNDropButton(QPushButton):
    def __init__(self, parent: QMainWindow, rg: ResourceGui): # pool is list wrapper `Pool`
        super().__init__(parent)
        self._super_rg = rg
        self.setAcceptDrops(True)
        self.setStyleSheet("border: none;")
        self.setIconSize(QSize(64, 64))
        self.resize(QSize(64, 64))
        pass


    def get_rg(self) -> ResourceGui:
        self._super_rg.get_resource().set_location((self.x(),self.y()))
        return self._super_rg


    def mouseMoveEvent(self, event):
        # if left mouse button is clicked 
        if event.buttons() == Qt.LeftButton:
            # create a mime object
            mimeData = QMimeData()
            # create a qdrag object
            drag = QDrag(self)
            # set mime object as the drag mime data 
            drag.setMimeData(mimeData)
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            # give drag the mouse transformation 
            _ = drag.exec_(Qt.MoveAction)
        pass


class TestResourceGui(unittest.TestCase):
    pass