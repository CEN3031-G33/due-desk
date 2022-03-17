# ------------------------------------------------------------------------------
# Project: DueDesk
# Module: due_desk
#
# Abstract: 
#   The main script called to begin the DueDesk application.
# ------------------------------------------------------------------------------

import unittest

from .window import *



def due_desk():
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