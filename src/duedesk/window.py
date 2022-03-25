import os
import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '../..'))
inventory = []
desk = []

@pyqtSlot()
def home_click():
    print('Home Button Clicked')

def tasks_click():
    print('Tasks Button Clicked')

def add_click():
    print('Add Task Button Clicked')

def zen_click():
    print('Zen Mode Button Clicked')

@pyqtSlot()
def item_move():
    print("item moved")

def start_task():
    print("hello")
   

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        screen = QApplication.primaryScreen()
        self.width = screen.size().width()
        self.height = screen.size().height()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.showFullScreen()

class MyTableWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
               
        
        img_path = root_dir + "\\resources\desk.jpg" 
        
        c_pixmap = QPixmap(img_path)
        c = QLabel(self)
        screen = QApplication.primaryScreen()
        c.resize(int(screen.size().width() * 0.8), int(screen.size().height() * 0.8))        
        c_scaledPixmap = c_pixmap.scaled(int(screen.size().width() * 0.8), int(screen.size().height() * 0.8), Qt.KeepAspectRatio, Qt.FastTransformation)        
        c.setPixmap(c_scaledPixmap)        
        c.setScaledContents(True)
        #self.__initButtons__()
        self.__initInventoryList__()
        self.__initTaskList__()
        self.__initDragButtons__()

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
        position = event.pos()
        event.source().move(position)
        event.accept()


# ^^^^ drag and drop ^^^^

    def displayButtons(self):
        for i in range(len(desk)):
            desk[i].show()

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
        group_box.setStyleSheet("text-align: center; font-size: 20px; font-family: Helevetica;")


        for i in range (0,50):
            item = QPushButton()
            item_pixmap = QIcon(root_dir + "\\resources\lamp.jpg")
            item.setIcon(item_pixmap)
            item.setIconSize(QSize(int(screen.size().width() * 0.1), int(screen.size().height() * 0.1)))
            item.clicked.connect(self.createButton)
            inventory.append(item)
            hbox.addWidget(inventory[i])

        group_box.setLayout(hbox)
        title = "Inventory (" + str(len(inventory)) + ")"
        group_box.setTitle(title)

        scroll = QScrollArea()
        scroll.setWidget(group_box)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(scroll)

        inv_list.setLayout(layout)

    def __initTaskList__(self):
        screen = QApplication.primaryScreen()
        task_list = QWidget(self)
        task_list.resize(int(screen.size().width() * 0.2), int(screen.size().height()))
        task_list.move(int(screen.size().width() * 0.8), 0)

        form_layout = QFormLayout()
        group_box = QGroupBox("My Tasks")
        group_box.setStyleSheet("text-align: center; font-size: 20px; font-family: Helevetica;")

        tasks = []
        task_buttons = []
        for i in range (0,50):
            tasks.append(QLabel("Task - this one is long and should take 2 lines"))
            button = QPushButton("Start")
            #button.clicked.connect(self.buttonClicked)
            task_buttons.append(button)
            form_layout.addRow(tasks[i], task_buttons[i])

        group_box.setLayout(form_layout)
        title = "My Tasks (" + str(len(tasks)) + ")"
        group_box.setTitle(title)
        scroll = QScrollArea()
        scroll.setWidget(group_box)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(scroll)

        task_list.setLayout(layout)

class Button(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)
        screen = QApplication.primaryScreen()
        QButton_icon = QIcon(root_dir + "\\resources\lamp.jpg")
        self.setIcon(QButton_icon)
        self.setIconSize(QSize(int(screen.size().width() * 0.1), int(screen.size().height() * 0.1)))
        self.setStyleSheet("border: none;")
        self.resize(QSize(int(screen.size().width() * 0.1), int(screen.size().height() * 0.1)))

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