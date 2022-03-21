from asyncio import Task
from operator import truediv
import os
import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '../..'))

@pyqtSlot()
def home_click():
    print('Home Button Clicked')

def tasks_click():
    print('Tasks Button Clicked')

def add_click():
    print('Add Task Button Clicked')

def zen_click():
    print('Zen Mode Button Clicked')


'''
def window():
    
    Example code to open a basic window to demonstrate pyqt5 is properly 
    installed.
    
    app = QApplication(sys.argv)
    screen = app.primaryScreen()

    w = QWidget()
    home_button = QPushButton('Home', w)
    home_button.move(0,0)
    home_button.clicked.connect(home_click)
    offset = home_button.width()
    tasks_button = QPushButton('Tasks', w)
    tasks_button.move(offset, 0)
    tasks_button.clicked.connect(tasks_click)
    offset += tasks_button.width()
    add_task_button = QPushButton('Add Task', w)
    add_task_button.move(offset, 0)
    add_task_button.clicked.connect(add_click)
    offset += add_task_button.width()
    zen_button = QPushButton('Zen Mode', w)
    zen_button.move(offset, 0)
    zen_button.clicked.connect(zen_click)

    b = QLabel(w)
    b.setText("Welcome to your DueDesk!")
    b.setStyleSheet(" font-size: 20px; font-family: Helvetica; background-color: brown; color: white;")
    b.setAlignment(QtCore.Qt.AlignLeft)
    b.move(int((screen.size().width())/2 - b.size().width()),int(screen.size().height()/20))
    c = QLabel(w)
    img_path = root_dir + "\\resources\desk.jpg"
    c_pixmap = QPixmap(img_path)
    c.setPixmap(c_pixmap.scaled(screen.size().width(), screen.size().height()))
    c.setScaledContents(True)
    b.raise_()
    home_button.raise_()
    tasks_button.raise_()
    add_task_button.raise_()
    zen_button.raise_()
    w.setWindowTitle("Due Desk")
    w.setFixedSize(screen.size().width(), screen.size().height())
    w.showMaximized()
    sys.exit(app.exec_()) 
'''    

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

        self.button = Button('My Image', self)
        self.button.move(50,50)

        #### drag and drop events ####
    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        position = event.pos()
        self.button.move(position)
        event.accept()

# ^^^^ drag and drop ^^^^

    def __initInventoryList__(self):
        screen = QApplication.primaryScreen()
        inv_list = QWidget(self)
        inv_list.resize(int(screen.size().width() * 0.8), int(screen.size().height() * 0.2))
        inv_list.move(0, int(screen.size().height() * 0.8))

        hbox = QHBoxLayout()
        group_box = QGroupBox("Inventory")
        group_box.setStyleSheet("text-align: center; font-size: 20px; font-family: Helevetica;")

        inventory = []

        for i in range (0,50):
            item = QLabel()
            item_pixmap = QPixmap(root_dir + "\\resources\lamp.jpg")
            item.setPixmap(item_pixmap.scaled(int(screen.size().width() * 0.1), int(screen.size().height() * 0.1), Qt.KeepAspectRatio, Qt.FastTransformation))
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

        for i in range (0,50):
            tasks.append(QLabel("Task"))
            form_layout.addRow(tasks[i])

        group_box.setLayout(form_layout)
        title = "My Tasks (" + str(len(tasks)) + ")"
        group_box.setTitle(title)
        scroll = QScrollArea()
        scroll.setWidget(group_box)
        scroll.setWidgetResizable(True)

        layout = QVBoxLayout()
        layout.addWidget(scroll)

        task_list.setLayout(layout)
    
            


    def __initButtons__(self):
        home_button = QPushButton('Home', self)
        home_button.move(0,0)
        home_button.clicked.connect(home_click)
        offset = home_button.width()
        tasks_button = QPushButton('Tasks', self)
        tasks_button.move(offset, 0)
        tasks_button.clicked.connect(tasks_click)
        offset += tasks_button.width()
        add_task_button = QPushButton('Add Task', self)
        add_task_button.move(offset, 0)
        add_task_button.clicked.connect(add_click)
        offset += add_task_button.width()
        zen_button = QPushButton('Zen Mode', self)
        zen_button.move(offset, 0)
        zen_button.clicked.connect(zen_click)

        home_button.raise_()
        tasks_button.raise_()
        add_task_button.raise_()
        zen_button.raise_()


class Button(QPushButton):
    def __init__(self, button_text, parent):
        super().__init__(button_text, parent)
        

    def mouseMoveEvent(self, event):
        # if left mouse button is clicked 
        if event.buttons() == Qt.LeftButton:
            
            # create a mime object
            mimeData = QMimeData()
            
            # create a qdrag object
            drag = QDrag(self)

            # set mime object as the drag mime data 
            drag.setMimeData(mimeData)

            # give drag the mouse transformation 
            dropAction = drag.exec_(Qt.MoveAction)