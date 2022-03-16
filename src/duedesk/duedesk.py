# ------------------------------------------------------------------------------
# Project: DueDesk
# Module: duedesk
#
# Abstract: 
#   The main script called to begin the DueDesk application.
# ------------------------------------------------------------------------------

import unittest
from .task import Task

def duedesk():
    print("Welcome to your DueDesk!")


def main():
    duedesk()


#--- entry-point ---
if __name__ == "__main__":
    main()


#--- unit-tests ----
class TestDueDesk(unittest.TestCase):

    def test_sample_unit(self):
        self.assertEqual(1 + 1, 2)