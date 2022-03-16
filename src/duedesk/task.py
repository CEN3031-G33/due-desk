# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : task
# Abstract : 
#   A task is a central object to the DueDesk. It stores information about
#   things a user should do and allows user's to input new tasks.
# ------------------------------------------------------------------------------
import unittest


class Task:
    def __init__(self, subject, deadline) -> None:
        '''Creates a new `Task` object.'''
        self._subject = subject
        self._deadline = deadline
        pass


    def get_subject(self) -> str:
        return self._subject


    def get_deadline(self) -> str:
        return self._deadline


    def set_subject(self, s) -> None:
        self._subject = s


    def set_deadline(self, d) -> None:
        self._deadline = d


    def __repr__(self) -> str:
        '''Represent `Task` as a str.'''
        repr = '\ntopic: '+self._subject+'\ndue: '+self._deadline+'\n\n'
        return repr
    pass


class TestTask(unittest.TestCase):
    def test_new(self):
        t = Task('write task class', '2022-01-01')
        self.assertEqual(t._subject, 'write task class')
        self.assertEqual(t._deadline, '2022-01-01')
        # print(t.__repr__())
        pass


    def test_modifiers_accessors(self):
        t = Task('nothing', 'never')

        self.assertEqual(t.get_subject(), 'nothing')
        self.assertEqual(t.get_deadline(), 'never')

        t.set_subject('read a book')
        self.assertEqual(t.get_subject(), 'read a book')

        t.set_deadline('2022-03-15')
        self.assertEqual(t.get_deadline(), '2022-03-15')

        pass
