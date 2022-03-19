# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : duedesk
# Abstract : 
#   The main script called to begin the DueDesk application.
# ------------------------------------------------------------------------------
import unittest
from .window import *

def due_desk():
    #window()
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    ex = App()
    sys.exit(app.exec_())


def main():
    due_desk()


if __name__ == "__main__":
    main()


class TestDueDesk(unittest.TestCase):
    def test_sample_unit(self):
        self.assertEqual(1 + 1, 2)
        pass
    pass