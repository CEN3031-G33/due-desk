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
#from .window import Button 

class ResourceGui(QWidget):
    def __init__(self, root: QMainWindow):
        '''Creates a `ResourceGui` instance.'''
        super(QWidget, self).__init__(root)
        self._button = QPushButton(self)
        self._button.setIconSize(QSize(64, 64))
        self._filepath = "./resources/pc.png"
        self._image = QIcon(self._filepath)
        self._button.setIcon(self._image)
        self._resource = Resource(self._filepath, (0, 0), False, False, 0)
        self._root = root
        pass


    def glue_to_gui(self, layout: QFormLayout):
        '''Attaches the PyQt5 gui elements to the layout.'''
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
        # return new object 
        # new object has drag and drop 
        rg = ResourceGui(self._root)
        rg.get_resource().set_filepath(self._filepath)
        rg._image =  self._image
        rg._button = Button(self._root)
        rg._button.setIcon(self._image)
        rg._button.move(10,10)
        rg._button.show()


        #return rg
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

class Button(QPushButton):
    
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        screen = QApplication.primaryScreen()
        #QButton_icon = QIcon(root_dir + "/resources/pc.png")

        self.setIconSize(QSize(int(screen.size().width() * 0.1), int(screen.size().height() * 0.1)))
        self.setStyleSheet("border: none;")
        self.resize(QSize(int(screen.size().width() * 0.1), int(screen.size().height() * 0.1)))
        '''
        # change the path lock and cost parameters here
        #self.imagePath = root_dir + "/resources/pc.png"
        self.locked = False
        self.cost = 0
        
        #self.setIcon(QButton_icon)
        self.setIconSize(QSize(int(screen.size().width() * 0.1), int(screen.size().height() * 0.1)))
        self.setStyleSheet("border: none;")
        self.resize(QSize(int(screen.size().width() * 0.1), int(screen.size().height() * 0.1)))
        #self.move(int(screen.size().width() * 0.8 - self.width()), int(screen.size().height() * 0.8 - self.height()))
        '''

 
    # create get method for file attribute 
    #def get_filepath(self) -> str:
    #    return self.fpButton

    '''def getX(self):
        return (self.x())

    def getY(self):
        return (self.y())

    def getImageName(self):
        return (self.imagePath)

    def getLockStatus(self):
        return (self.locked)

    def getCost(self):
        return (self.cost)'''
    


    
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
            dropAction = drag.exec_(Qt.MoveAction)