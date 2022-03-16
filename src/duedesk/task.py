# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : task
# Abstract : 
#   A task is a central object to the DueDesk. It stores information about
#   things a user should do and allows user's to input new tasks.
# ------------------------------------------------------------------------------
import unittest

class Task:
    def __init__(self):
        self.subject = ''
        self.deadline = ''
        pass

    pass


class TestTask(unittest.TestCase):
    def new(self):
        self.assertEqual(1 + 1, 2)