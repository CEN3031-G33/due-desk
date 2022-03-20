# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : resource
# Abstract : 
#   Object that user can add, remove, and move around the desk.
#   The objects are loaded from external files
# ------------------------------------------------------------------------------

import unittest
import os
from typing import Tuple

class Resource:
    def __init__(self, filepath: str, location: Tuple[float, float], locked: bool, inscene: bool) -> None:
        self.set_filepath(filepath)
        self._location = location
        self._islocked = locked
        self._inscene = inscene
        pass
    pass

    def get_filepath(self) -> str:
        return self._filepath

    def get_location(self) -> Tuple[float, float]:
        return self._location

    def is_locked(self) -> bool:
        return self._islocked
    
    def is_inscene(self) -> bool:
        return self._inscene

    def set_filepath(self, f: str) -> bool:
        '''Returns whether filepath exists'''
        if os.path.exists(f) and os.path.isfile(f):
            self._filepath = f
            return True
        else:
            self._filepath = ""
            return False
    
    def set_location(self, l: Tuple[float, float]):
        self._location = l

    def set_islocked(self, l: bool):
        self._islocked = l

    def set_inscene(self, i: bool):
        self._inscene = i

class TestResource(unittest.TestCase): 
    def test_init(self):
        r = Resource("file", [1,1], False, False)
        self.assertEqual("", r._filepath)
        self.assertEqual([1,1], r._location)
        self.assertEqual(False, r._islocked)
        self.assertEqual(False, r._inscene)

    def test_filepath(self):
        r = Resource("", [1,1], False, False)
        self.assertFalse(r.set_filepath("dud"))
        self.assertTrue(r.set_filepath("./docs/images/superdesk.png"))

    

    pass