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
        self._minutes = 0.0
        pass


    def to_dict(self) -> dict:
        '''Serializes `Task` object into json-compatible `dict`.'''
        data = {
            'subject': self.get_subject(),
            'deadline': str(self.get_deadline()),
            'complete': str(self.is_complete()),
            'minutes': str(self.get_minutes())
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
                # note: account for invalid deadline loaded... t.get_deadline().is_valid()
            elif k == 'complete':
                t.set_complete(v == "True")
            elif k == 'minutes':
                t.add_minutes(float(v))
        return t


    def partial_eq(self, other) -> bool:
        '''Evaluates if two `Task` objects have the same deadline and subject data.'''
        return self.get_deadline() == other.get_deadline() and \
            self.get_subject() == other.get_subject()


    def get_subject(self) -> str:
        return self._subject


    def get_deadline(self) -> Deadline:
        return self._deadline


    def get_minutes(self) -> float:
        return self._minutes


    def is_complete(self) -> bool:
        return self._complete


    def set_subject(self, s: str) -> None:
        self._subject = s

    
    def add_minutes(self, m: float) -> None:
        self._minutes += m


    def set_deadline(self, d: Deadline) -> None:
        self._deadline = d


    def set_complete(self, c: bool) -> None:
        self._complete = c


    def get_key(self) -> str:
        '''Returns a `Task` objects unique key representation.'''
        return self.get_subject()+str(self.get_deadline())


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


    def test_add_minutes(self):
        t = Task('A', Deadline(2022, 1, 1))
        self.assertEqual(t.get_minutes(), 0.0)
        t.add_minutes(1.0)
        self.assertEqual(t.get_minutes(), 1.0)
        t.add_minutes(15.7)
        self.assertEqual(t.get_minutes(), 16.7)
        pass


    def test_to_dict(self):
        t = Task('write a book', Deadline(2022, 1, 1))
        t.set_complete(True)
        t.add_minutes(10.2)
        self.assertEqual(t.to_dict(), 
        {
            "complete": "True", 
            "subject": "write a book", 
            "minutes": '10.2', 
            "deadline": "2022-01-01"
        })
        pass

    
    def test_from_dict(self):
        data = {
            "subject": "write a book",
            "deadline": "2022-01-01",
            "complete": "True",
            "minutes": "60.4",
        }
        t = Task('write a book', Deadline(2022, 1, 1))
        self.assertTrue(Task.from_dict(data).partial_eq(t))
        self.assertEqual(Task.from_dict(data).is_complete(), True)
        self.assertEqual(Task.from_dict(data).get_minutes(), 60.4)
        data = {
            "subject": "write a book",
            "deadline": "2022-01-01",
            "complete": "False",
            "minutes": "60.4",
        }
        t = Task('write a book', Deadline(2022, 1, 1))
        self.assertTrue(Task.from_dict(data).partial_eq(t))
        self.assertEqual(Task.from_dict(data).is_complete(), False)
        self.assertEqual(Task.from_dict(data).get_minutes(), 60.4)
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