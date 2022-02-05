# ------------------------------------------------------------------------------
# Project: DueDesk
# Module: due_desk
#
# Abstract: 
#   The main script called to begin the DueDesk application.
# ------------------------------------------------------------------------------

import unittest

def due_desk():
    print("Welcome to your DueDesk!")


def main():
    due_desk()


#--- entry-point ---
if __name__ == "__main__":
    main()


#--- unit-tests ----
class TestDueDesk(unittest.TestCase):

    def test_sample_unit(self):
        self.assertEqual(1 + 1, 2)