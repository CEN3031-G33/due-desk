# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : task
# Abstract : 
#   A task is a central object to the DueDesk. It stores information about
#   things a user should do and allows user's to input new tasks.
# ------------------------------------------------------------------------------
import unittest
from .deadline import Deadline

class Task:
    def __init__(self, subject: str, deadline: Deadline) -> None:
        '''Creates a new `Task` object.'''
        self._subject = subject
        self._deadline = deadline
        self._complete = False
        # :todo: add a '_progress` attribute that stores time worked on task
        pass


    def to_dict(self) -> dict:
        '''Serializes `Task` object into json-compatible `dict`.'''
        data = {
            'subject': self._subject,
            'deadline': str(self._deadline),
            'complete': str(self._complete)
        }
        return data


    @classmethod
    def from_dict(cls, data: dict):
        '''Deserializes a `dict` loaded from json into a `Task` object.'''
        t = Task('', '')
        for (k, v) in data.items():
            if k == 'subject':
                t.set_subject(v)
            elif k == 'deadline':
                t.set_deadline(Deadline.from_str(v))
            elif k == 'complete':
                t.set_complete(bool(v))
        return t


    def partial_eq(self, other) -> bool:
        '''Evaluates if two `Task` objects have the same deadline and subject data.'''
        return self.get_deadline() == other.get_deadline() and \
            self.get_subject() == other.get_subject()


    def get_subject(self) -> str:
        return self._subject


    def get_deadline(self) -> Deadline:
        return self._deadline


    def is_complete(self) -> bool:
        return self._complete


    def set_subject(self, s: str) -> None:
        self._subject = s


    def set_deadline(self, d: Deadline) -> None:
        self._deadline = d


    def set_complete(self, c: bool) -> None:
        self._complete = c


    def __str__(self) -> str:
        '''Print `Task` as a str.'''
        repr = 'topic: '+self._subject+'\tdue: '+str(self._deadline)+'\n'
        return repr
    pass


class TestTask(unittest.TestCase):
    def test_new(self):
        t = Task('write task class', Deadline(2022, 1, 1))
        self.assertEqual(t._subject, 'write task class')
        self.assertEqual(t._deadline, Deadline(2022, 1, 1))
        self.assertEqual(t._complete, False)
        pass


    def test_modifiers_accessors(self):
        t = Task('nothing', Deadline(0, 0, 0))
        self.assertEqual(t.get_subject(), 'nothing')
        self.assertEqual(t.get_deadline(), Deadline(0, 0, 0))

        t.set_subject('read a book')
        self.assertEqual(t.get_subject(), 'read a book')

        t.set_deadline(Deadline(2022, 3, 15))
        self.assertEqual(t.get_deadline(), Deadline(2022, 3, 15))

        self.assertEqual(t.is_complete(), False)
        t.set_complete(True)
        self.assertEqual(t.is_complete(), True)
        pass


    def test_to_dict(self):
        t = Task('write a book', Deadline(2022, 1, 1))
        t.set_complete(True)
        self.assertEqual(t.to_dict(), 
        {"complete": "True", "subject": "write a book", "deadline": "2022-01-01"})
        pass

    
    def test_from_dict(self):
        data = {
            "subject": "write a book",
            "deadline": "2022-01-01",
            "complete": "True",
        }
        t = Task('write a book', Deadline(2022, 1, 1))
        t.set_complete(True)
        self.assertTrue(Task.from_dict(data).partial_eq(t))
        self.assertTrue(Task.from_dict(data).is_complete(), True)
        pass


    def test_partial_eq(self):
        # pointing to different addresses in memory
        t0 = Task('A', Deadline(2022, 1, 1))
        t1 = Task('A', Deadline(2022, 1, 1))
        self.assertNotEqual(t0, t1)
        self.assertTrue(t0.partial_eq(t1))

        t1 = Task('B', Deadline(2022, 1, 1))
        self.assertNotEqual(t0, t1)
        self.assertFalse(t0.partial_eq(t1))

        t1 = Task('A', Deadline(2022, 1, 2))
        self.assertNotEqual(t0, t1)
        self.assertFalse(t0.partial_eq(t1))

        # pointing to same address in memory
        t1 = t0
        self.assertEqual(t0, t1)
        self.assertTrue(t0.partial_eq(t1))
        pass
    pass