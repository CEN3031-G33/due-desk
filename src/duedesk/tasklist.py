# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : tasklist
# Abstract : 
#   A tasklist is the manager of multiple tasks. It allows users to interact
#   with a common group of tasks.
# ------------------------------------------------------------------------------
import unittest
import json
from typing import List
from .task import Task
from .deadline import Deadline

# :wip:
class Tasklist:
    def __init__(self, inner: List[Task]):
        '''Creates a `Tasklist` object.'''
        self._inner = inner
        pass


    # :todo: test and impl
    @classmethod
    def from_dict(cls, data: dict):
        '''Converts a python dictionary loaded from json into a `Tasklist` object.'''
        tl = Tasklist()
        return tl

    
    def get_by_index(self, i: int) -> Task:
        '''Access the `Task` at index `i`. Returns `None` if `i` is an invalid index.'''
        if i >= len(self._inner) or i < 0:
            return None
        return self._inner[i]


    def to_dict(self) -> dict:
        '''Converts `Tasklist` object into json-compatible `dict`.'''
        data = {}
        # :todo: maybe a better way to store in json instead of by index?
        # maybe move `subject` to be a task's key in the `dict`.
        i = 0
        for t in self._inner:
            data[str(i)] = t.to_dict()
            i += 1
        return data
    pass


class TestTasklist(unittest.TestCase):
    def test_new_and_get_by_index(self):
        tl = Tasklist([
            Task('A', Deadline(2022, 1, 1)),
            Task('B', Deadline(2022, 1, 2)),
            Task('C', Deadline(2022, 1, 3)),
            ])
        self.assertTrue(tl.get_by_index(0).partial_eq(Task('A', Deadline(2022, 1, 1))))
        self.assertTrue(tl.get_by_index(2).partial_eq(Task('C', Deadline(2022, 1, 3))))
        self.assertTrue(tl.get_by_index(3) == None)
        self.assertTrue(tl.get_by_index(-1) == None)
        pass


    def test_to_dict(self):
        tl = Tasklist([
            Task('A', Deadline(2022, 1, 1)),
            Task('B', Deadline(2022, 1, 2)),
            Task('C', Deadline(2022, 1, 3)),
            ])

        self.assertEqual(tl.to_dict(), 
        {
            "0": {
                "subject": "A",
                "deadline": "2022-01-01"
            },
            "1": {
                "subject": "B",
                "deadline": "2022-01-02"
            },
            "2": {
                "subject": "C",
                "deadline": "2022-01-03"
            }
        })
        pass
    pass