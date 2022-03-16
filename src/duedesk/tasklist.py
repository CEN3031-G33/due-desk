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
    def add(self, t: Task) -> bool:
        '''Adds a new `Task` to the list. Returns `false` if a task with the same
        subject already exists.'''
        return False


    @classmethod
    def from_dict(cls, data: dict):
        '''Deserializes a `dict` loaded from json into a `Tasklist` object.'''
        tasks = []
        for v in data.values():
            tasks += [Task.from_dict(v)]
        tl = Tasklist(tasks)
        return tl


    def to_dict(self) -> dict:
        '''Serializes `Tasklist` object into json-compatible `dict`.'''
        data = {}
        # :todo: maybe a better way to store in json instead of by index?
        #   maybe move `subject` to be a task's key in the `dict`.
        i = 0
        for t in self._inner:
            data[str(i)] = t.to_dict()
            i += 1
        return data


    def get_by_index(self, i: int) -> Task:
        '''Access the `Task` at index `i`. Returns `None` if `i` is an invalid index.'''
        if i >= len(self._inner) or i < 0:
            return None
        return self._inner[i]


    def __eq__(self, o) -> bool:
        '''Performs in-order element-wise partial equality check on `Tasks`.'''
        if len(self._inner) != len(o._inner):
            return False
        else:
            for i in range(0, len(self._inner)):
                if not self._inner[i].partial_eq(o._inner[i]):
                    return False
        return True
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


    def test_from_dict(self):
        data = {
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
        }
        self.assertEqual(Tasklist.from_dict(data), Tasklist([
            Task('A', Deadline(2022, 1, 1)),
            Task('B', Deadline(2022, 1, 2)),
            Task('C', Deadline(2022, 1, 3)),
            ]))
        pass
    pass