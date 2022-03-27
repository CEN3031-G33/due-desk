# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : tasklist
# Abstract : 
#   A tasklist is the manager of multiple tasks. It allows users to interact
#   with a common group of tasks.
# ------------------------------------------------------------------------------
import unittest
from typing import List
from .task import Task
from .deadline import Deadline

class Tasklist:
    def __init__(self, inner: List[Task]):
        '''Creates a `Tasklist` object.'''
        self._inner = inner
        pass
    

    def add(self, t: Task) -> bool:
        '''Adds a new `Task` to the list and resorts the list. Returns `false` if a task with the same
        subject and same deadline already exists.'''
        # check for existing equivalent task
        for x in self._inner:
            if x.partial_eq(t):
                return False
        # append to the list
        self._inner.append(t)
        # sort items according to earliest-deadline-first
        self.sort()
        return True


    def sort(self) -> None:
        '''Sorts the `Task` objects according to their deadlines, using the `earliest-deadline-first`
        approach. This is a greedy approach that optimizes for minimal lateness.'''
        self._inner.sort(key=lambda task: task.get_deadline())
        pass


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
        for t in enumerate(self._inner):
            data[str(t[0])] = t[1].to_dict()
        return data


    def get_by_index(self, i: int) -> Task:
        '''Access the `Task` at index `i`. Returns `None` if `i` is an invalid index.'''
        if i >= len(self._inner) or i < 0:
            return None
        return self._inner[i]


    def __len__(self) -> int:
        return len(self._inner)


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
        # index out-of-bounds errors
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
                "complete": "False",
                "subject": "A",
                "minutes": '0.0',
                "deadline": "2022-01-01"
            },
            "1": {
                "complete": "False",
                "subject": "B",
                "minutes": '0.0',
                "deadline": "2022-01-02"
            },
            "2": {
                "complete": "False",
                "subject": "C",
                "minutes": '0.0',
                "deadline": "2022-01-03"
            }
        })
        pass


    def test_from_dict(self):
        data = {
            "0": {
                "subject": "A",
                "deadline": "2022-01-01",
                "minutes": '0.0',
                "complete": "False",
            },
            "1": {
                "subject": "B",
                "deadline": "2022-01-02",
                "minutes": '0.0',
                "complete": "False",
            },
            "2": {
                "subject": "C",
                "deadline": "2022-01-03",
                "minutes": '0.0',
                "complete": "False",
            }
        }
        self.assertEqual(Tasklist.from_dict(data), Tasklist([
            Task('A', Deadline(2022, 1, 1)),
            Task('B', Deadline(2022, 1, 2)),
            Task('C', Deadline(2022, 1, 3)),
            ]))
        pass


    def test_sort(self):
        tl = Tasklist([
            Task('A', Deadline(2022, 1, 8)),
            Task('B', Deadline(2022, 1, 4)),
            Task('C', Deadline(2022, 1, 5)),
            ])
        tl.sort()
        self.assertEqual(tl, Tasklist([
            Task('B', Deadline(2022, 1, 4)),
            Task('C', Deadline(2022, 1, 5)),
            Task('A', Deadline(2022, 1, 8)),
        ]))
        pass


    def test_add(self):
        tl = Tasklist([
            Task('A', Deadline(2022, 1, 4)),
            Task('B', Deadline(2022, 1, 5)),
            Task('C', Deadline(2022, 1, 8)),
            ])
        # adds a new task to the task list
        result = tl.add(Task('D', Deadline(2022, 1, 6)))
        self.assertTrue(result)
        self.assertEqual(tl, Tasklist([
            Task('A', Deadline(2022, 1, 4)),
            Task('B', Deadline(2022, 1, 5)),
            Task('D', Deadline(2022, 1, 6)),
            Task('C', Deadline(2022, 1, 8)),
            ]))
        # fails to add an already equivalent task
        result = tl.add(Task('A', Deadline(2022, 1, 4)))
        self.assertFalse(result)
        self.assertEqual(tl, Tasklist([
            Task('A', Deadline(2022, 1, 4)),
            Task('B', Deadline(2022, 1, 5)),
            Task('D', Deadline(2022, 1, 6)),
            Task('C', Deadline(2022, 1, 8)),
            ]))
        pass
    pass