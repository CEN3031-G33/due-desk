import os
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

root_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), '../..'))

def window():
    '''
    Example code to open a basic window to demonstrate pyqt5 is properly 
    installed.
    '''
    app = QApplication(sys.argv)
    screen = app.primaryScreen()

    w = QWidget()
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
    w.setWindowTitle("Due Desk")
    w.setFixedSize(screen.size().width(), screen.size().height())
    w.showMaximized()
    sys.exit(app.exec_())
