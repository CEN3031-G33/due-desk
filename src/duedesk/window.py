
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import webbrowser
from .desk import Desk
import unittest
from .resourcegui import ResourceGui

root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '../..'))
root_dir = '.'
inventory = []
desk = []
trash_pos = QRect()

@pyqtSlot()
def start_task():
    print("hello")   

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Due Deskdue'
        self.left = 0
        self.top = 0
        screen = QApplication.primaryScreen()
        self.width = screen.size().width()
        self.height = screen.size().height()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.drawMenu()
        self.showFullScreen()
        #self.setFixedSize(self.layout.sizeHint())
        

    def drawMenu(self):
        self.menu_widget = menuScreen(self)
        self.setCentralWidget(self.menu_widget)

    def drawTable(self):
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

class menuScreen(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.setAutoFillBackground(True)
        p = self.palette()
        color = QColor().fromRgb(qRgb(210, 180, 140))
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

        img_path = root_dir + "/resources/title.png" 
        c_pixmap = QPixmap(img_path)
        c = QLabel(self)
        screen = QApplication.primaryScreen()
        c.resize(int(screen.size().width() * 0.3), int(screen.size().height() * 0.3))        
        c_scaledPixmap = c_pixmap.scaled(int(screen.size().width() * 0.4), int(screen.size().height() * 0.4), Qt.KeepAspectRatio, Qt.FastTransformation)        
        c.setPixmap(c_scaledPixmap)
        c.setScaledContents(True)
        c.move(int(screen.size().width()/2 - c.width()/2), int(screen.size().height()/2 - c.height()*1.2))

        start_button = QPushButton(self)
        start_button.setText("Start")
        start_button.move(int(screen.size().width()/2 - start_button.width() * 1.5), int(screen.size().height()/2))
        start_button.clicked.connect(lambda:self.enterDesk(parent))

        help_button = QPushButton(self)
        help_button.setText("Help")
        help_button.move(int(screen.size().width()/2), int(screen.size().height()/2))
        help_button.clicked.connect(self.help)

    def enterDesk(self, parent):
        self.close()
        parent.drawTable()
        return True

    def help(self):
        webbrowser.open('https://github.com/CEN3031-G33/due-desk')
        return 'https://github.com/CEN3031-G33/due-desk'

class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        # boot up the due desk!
        dd = Desk('./tests/data.json', parent)
        dd.load_from_file()

        self._parent = parent
        self.__initTable__()
        self.__initInventoryList__()
        self.__initDragButtons__()

    def __initTable__(self):
        img_path = root_dir + "/resources/pixel-desk.png" 
        
        c_pixmap = QPixmap(img_path)
        c = QLabel(self)
        screen = QApplication.primaryScreen()
        c.resize(int(screen.size().width() * 0.8), int(screen.size().height() * 0.8))        
        c_scaledPixmap = c_pixmap.scaled(int(screen.size().width() * 0.8), int(screen.size().height() * 0.8), Qt.KeepAspectRatio, Qt.FastTransformation)        
        c.setPixmap(c_scaledPixmap)        
        c.setScaledContents(True)

        paint_path = root_dir + "/resources/paint-bucket.png"
        paint_icon = QIcon(paint_path)
        paint = QPushButton(self)
        paint.setIcon(paint_icon)
        paint.setIconSize(QSize(int(screen.size().width() * 0.05), int(screen.size().height() * 0.05)))
        paint.move(int(screen.size().width() * 0.75), 10)
        paint.clicked.connect(self.setColor)
        paint.setStyleSheet("border: none;")

        exit_button = QPushButton(self)
        exit_button.setText("Exit")
        exit_button.clicked.connect(self.exitDesk)

        trash_path = root_dir + "/resources/trash.png"
        trash_widget = QLabel(self)
        trash_widget_pixmap = QPixmap(trash_path)
        trash_widget.resize(int(screen.size().width() * 0.15), int(screen.size().height() * 0.15))
        trash_widget.setPixmap(trash_widget_pixmap.scaled(int(screen.size().width() * 0.15), int(screen.size().height() * 0.15), Qt.KeepAspectRatio, Qt.FastTransformation))
        trash_widget.move(0, int(screen.size().height() * 0.65))

        trash_pos = trash_widget.geometry()

    def __initDeskLayout__():
        foo = 1

# vvvv drag and drop vvvv

    def __initDragButtons__(self):
        # needed to allow drops on application window
        self.setAcceptDrops(True)

        for i in range(len(desk)):
            btn = Button(self)
        #self.button = Button(self)
        #self.button.move(50,50)

        #### drag and drop events ####

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        screen = QApplication.primaryScreen()
        position = event.pos()
        trash_size = QSize(int(screen.size().width() * 0.15), int(screen.size().height() * 0.15))
        trash_point = QPoint(0, int(screen.size().height() * 0.65) )
        trash_rect = QRect(trash_point, trash_size)
        if (trash_rect.contains(position)):
            desk.remove(event.source())
            event.source().deleteLater()
            return
        event.source().move(position)
        event.accept()
            

# ^^^^ drag and drop ^^^^

    def displayButtons(self):
        for i in range(len(desk)):
            desk[i].show()

    def saveButtons(self):
        # send button values to resource class 
        # values needed:
        # filepath: str, location: Tuple[float, float], locked: bool, inscene: bool, cost: int
        print("printing all button positions")
        for i in range(len(desk)):
            button = desk[i]
            #print(button.get_filepath())
            print(button.x(), button.y())
            

    def createButton(self):
        desk.append(Button(self))
        self.displayButtons()

    def __initInventoryList__(self):
        screen = QApplication.primaryScreen()
        inv_list = QWidget(self)
        inv_list.resize(int(screen.size().width() * 0.8), int(screen.size().height() * 0.2))
        inv_list.move(0, int(screen.size().height() * 0.8))

        hbox = QHBoxLayout()
        group_box = QGroupBox("Inventory")
        group_box.setStyleSheet("text-align: center; font-size: 10px; font-family: Menlo;")

        for _ in range (0,50):
            ResourceGui(self).glue_to_gui(hbox)

        group_box.setLayout(hbox)
        title = "Inventory (" + str(len(inventory)) + ")"
        group_box.setTitle(title)

        scroll = QScrollArea()
        scroll.setWidget(group_box)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(scroll)

        inv_list.setLayout(layout)


    def setColor(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        color = QColorDialog.getColor()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

    def boxDesk(self):
        self.close()
        self.saveButtons()
        QApplication.quit()
        return True


class Button(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        screen = QApplication.primaryScreen()
        QButton_icon = QIcon(root_dir + "/resources/pc.png")

        #create a filepath Button attribute so it can be accesed later 
        #fpButton = Button()
        #fpButton.filepath = QButton_icon

        
        self.setIcon(QButton_icon)
        self.setIconSize(QSize(int(screen.size().width() * 0.1), int(screen.size().height() * 0.1)))
        self.setStyleSheet("border: none;")
        self.resize(QSize(int(screen.size().width() * 0.1), int(screen.size().height() * 0.1)))
        self.move(int(screen.size().width() * 0.8 - self.width()), int(screen.size().height() * 0.8 - self.height()))

 
    # create get method for file attribute 
    #def get_filepath(self) -> str:
    #    return self.fpButton

    def getX(self):
        return (self.x())

    def getY(self):
        return (self.y())

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

'''
class TestGui(unittest.TestCase):
    def test_menu(self):
        m = menuScreen(QMainWindow)
        self.assertTrue(m.enterDesk())
    
    def test_helpbutton(self):
        m = menuScreen(QMainWindow)
        self.assertEqual(m.help(), 'https://github.com/CEN3031-G33/due-desk')

    def test_exitdesk(self):
        t = MyTableWidget(QMainWindow)
        self.assertTrue(t.exitDesk())

    def test_buttonlocation(self):
        b = Button(QPushButton(QWidget(QMainWindow)))
        self.assertEqual(b.getX(), 0)
        self.assertEqual(b.getY(), 0)
        '''