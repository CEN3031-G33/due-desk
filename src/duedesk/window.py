import os
import sys
from PyQt5 import QtCore
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

def window():
    '''
    Example code to open a basic window to demonstrate pyqt5 is properly 
    installed.
    '''
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
