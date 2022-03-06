# ------------------------------------------------------------------------------
# Project: DueDesk
# Module: due_desk
#
# Abstract: 
#   The main script called to begin the DueDesk application.
# ------------------------------------------------------------------------------

import unittest

import os
import sys
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
    w = QWidget()
    b = QLabel(w)
    b.setText("Welcome to your DueDesk!")
    b.setStyleSheet(" font-size: 20px; font-family: Helvetica;")
    b.move(180,5)
    c = QLabel(w)
    img_path = root_dir + "\\resources\desk.jpg"
    c_pixmap = QPixmap(img_path)
    c.setPixmap(c_pixmap)
    w.resize(c_pixmap.width(), c_pixmap.height())
    b.raise_()
    w.setWindowTitle("Due Desk")
    w.show()
    sys.exit(app.exec_())


def due_desk():
    print("Welcome to your DueDesk!")
    window()

def main():
    due_desk()


#--- entry-point ---
if __name__ == "__main__":
    main()


#--- unit-tests ----
class TestDueDesk(unittest.TestCase):

    def test_sample_unit(self):
        self.assertEqual(1 + 1, 2)