# ------------------------------------------------------------------------------
# Project: DueDesk
# Module: due_desk
#
# Abstract: 
#   The main script called to begin the DueDesk application.
# ------------------------------------------------------------------------------

import unittest

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def window():
    '''
    Example code to open a basic window to demonstrate pyqt5 is properly 
    installed.
    '''
    app = QApplication(sys.argv)
    w = QWidget()
    b = QLabel(w)
    b.setText("Welcome to your DueDesk!")
    w.setGeometry(100,100,200,50)
    b.move(50,20)
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