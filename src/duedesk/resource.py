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
    def __init__(self, filepath: str, location: Tuple[float, float], locked: bool, inscene: bool, cost: int) -> None:
        '''Creates a `Resource` object.'''
        self._filepath = filepath
        self._location = location
        self._locked = locked
        self._inscene = inscene
        self.set_cost(cost)
        pass


    def is_filepath_valid(self) -> bool:
        '''Checks if the `filepath` is an existing file and has a proper image 
        extension: `.jpg`, `.png`.'''
        f = self.get_filepath()
        exts = ['.jpg', '.png']
        return os.path.exists(f) and os.path.isfile(f) and \
            os.path.splitext(f)[1].lower() in exts


    def to_dict(self) -> dict:
        '''Serializes `Resource` object into json-compatible `dict`.'''
        d = {
            "path": self._filepath, 
            "pixelmap": str(self._location), 
            "locked": str(self._locked), 
            "inscene": str(self._inscene),
            "cost": str(self._cost)
            }
        return d
        pass


    @classmethod
    def from_dict(cls, data: dict):
        '''Deserializes a `dict` loaded from json into a `Resource` object.'''
        r = Resource(data["path"], \
             tuple(map(float, data["pixelmap"].strip("(").strip(")").split(', '))), \
             data["locked"] == "True", \
             data["inscene"] == "True", \
             int(data["cost"]))
        return r
        pass

      
    def partial_eq(self, other) -> bool:
        '''Evaluates if two `Resource` objects have the same filepaths.'''
        return self._filepath == other._filepath
      

    def get_filepath(self) -> str:
        return self._filepath


    def get_location(self) -> Tuple[float, float]:
        return self._location


    def is_locked(self) -> bool:
        return self._locked


    def full_eq(self, other) -> bool:
        '''Compares filepaths, location, and cost of 2 resources.'''
        return self.partial_eq(other) and \
            self._location == other._location and \
            self._cost == other._cost
    

    def is_inscene(self) -> bool:
        return self._inscene

    def get_cost(self) -> int:
        return self._cost


    def set_filepath(self, f: str) -> None:
        self._filepath = f


    def set_location(self, l: Tuple[float, float]):
        self._location = l


    def set_locked(self, l: bool):
        self._locked = l


    def set_inscene(self, i: bool):
        self._inscene = i

    def set_cost(self, c: int):
        if c < 0:
            self._cost = 0
        else:
            self._cost = c
    pass


class TestResource(unittest.TestCase): 
    def test_init(self):
        r = Resource("file", (1, 2), True, False, 3)
        self.assertEqual("file", r._filepath)
        self.assertEqual((1, 2), r._location)
        self.assertEqual(True, r._locked)
        self.assertEqual(False, r._inscene)
        self.assertEqual(3, r._cost)
        pass


    def test_to_dict(self):
        r = Resource("file", (1, 2), True, False, 3)
        self.assertEqual(r.to_dict(), 
        {
            "path": "file", 
            "pixelmap": "(1, 2)", 
            "locked": 'True', 
            "inscene": "False",
            "cost": "3"
        })
        pass
    
    
    def test_full_eq(self):
        r0 = Resource("file", (1, 2), True, False, 3)
        r1 = Resource("file", (1, 2), True, False, 3)
        self.assertEqual(r0.full_eq(r1), True)
        # differing filepaths
        r1 = Resource("file2", (1, 2), True, False, 3)
        self.assertEqual(r0.full_eq(r1), False)
        # differing inscene and locked (don't care)
        r1 = Resource("file", (1, 2), False, True, 3)
        self.assertEqual(r0.full_eq(r1), True)
        # differing cost (bad)
        r1 = Resource("file", (1, 2), True, False, 7)
        self.assertEqual(r0.full_eq(r1), False)
        # differing x location (bad)
        r1 = Resource("file", (9, 2), True, False, 3)
        self.assertEqual(r0.full_eq(r1), False)
        # differing y location (bad)
        r1 = Resource("file", (1, 4), True, False, 3)
        self.assertEqual(r0.full_eq(r1), False)
        pass

      
    def test_from_dict(self):
        d = {
            "path": "file", 
            "pixelmap": "(1.5, 2.5)", 
            "locked": 'True', 
            "inscene": "False",
            "cost": "3"
            }
        r0 = Resource.from_dict(d)
        r1 = Resource("file", (1.5, 2.5), True, False, 3)
        self.assertEqual(r0._filepath, r1._filepath)
        self.assertEqual(r0._location, r1._location)
        self.assertEqual(r0._locked, r1._locked)
        self.assertEqual(r0._inscene, r1._inscene)
        self.assertEqual(r0._cost, r1._cost)

        d = {
            "path": "file", 
            "pixelmap": "(1.5, 2.5)", 
            "locked": 'True', 
            "inscene": "False",
            "cost": "-3"
            }
        r0 = Resource.from_dict(d)
        r1 = Resource("file", (1.5, 2.5), True, False, -10)
        self.assertEqual(r0._filepath, r1._filepath)
        self.assertEqual(r0._location, r1._location)
        self.assertEqual(r0._locked, r1._locked)
        self.assertEqual(r0._inscene, r1._inscene)
        self.assertEqual(r0._cost, r1._cost)
        pass


    def test_partial_eq(self):
        r0 = Resource("file", (1, 2), True, False, 3)
        r1 = Resource("dud", (1, 2), True, False, 3)
        self.assertFalse(r0.partial_eq(r1))
        self.assertFalse(r0 == r1)

        r1 = Resource("file", (1.4, 2.2), False, True, -4)
        self.assertTrue(r0.partial_eq(r1))
        self.assertFalse(r0 == r1)
        pass
        
        
    def test_accessors_modifiers(self):
        r = Resource("file", (1, 2), True, False, 3)
        self.assertEqual(r.get_location()[0], 1)
        self.assertEqual(r.get_location()[1], 2)
        self.assertEqual(r.get_filepath(), "file")
        self.assertEqual(r.is_inscene(), False)
        self.assertEqual(r.is_locked(), True)
        self.assertEqual(r.get_cost(), 3)

        r.set_location((9.0, 42.3))
        self.assertEqual(r.get_location()[1], 42.3)
        self.assertEqual(r.get_location()[0], 9.0)

        r.set_locked(False)
        self.assertEqual(r.is_locked(), False)

        r.set_inscene(True)
        self.assertEqual(r.is_inscene(), True)

        r.set_filepath("file2")
        self.assertEqual(r.get_filepath(), "file2")

        r.set_cost(-3)
        self.assertEqual(r.get_cost(), 0)
        r.set_cost(3)
        self.assertEqual(r.get_cost(), 3)
        pass


    def test_filepath(self):
        r = Resource("", (1, 1), False, False, 3)
        # set a non-existent file
        r.set_filepath("dud")
        self.assertFalse(r.is_filepath_valid())
        # set an existing file but not an image
        r.set_filepath("./README.md")
        self.assertFalse(r.is_filepath_valid())
        # set an existing file that is a proper image
        r.set_filepath("./docs/images/superdesk.png")
        self.assertTrue(r.is_filepath_valid())
        pass

    pass