# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : Resourcepool
# Abstract : 
#   A resource list is a manager of multiple resources. It will be used to
#   represent the pool of items the user can add to their desk and the items
#   currently on the desk.
# ------------------------------------------------------------------------------

import unittest
from typing import List
from .resource import Resource

class Resourcepool:
    def __init__(self, inner: List[Resource]):
        '''Creates a 'Resourcelist' object'''
        self._inner = inner
        pass

    def get_by_index(self, i: int) -> Resource:
        '''Access the `Resource` at index `i`. Returns `None` if `i` is an invalid index.'''
        if i >= len(self._inner) or i < 0:
            return None
        return self._inner[i]

class TestResourcelist(unittest.TestCase):
    def test_new_and_get_by_index(self):
        rl = Resourcepool([
            Resource("file", (1, 2), True, False, 3),
            Resource("./README.md", (1, 2), True, False, 3),
            Resource("./docs/images/superdesk.png", (1, 2), True, False, 3)
            ])
