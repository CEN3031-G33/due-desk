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
        '''Creates a `Resource` object.'''
        self._filepath = filepath
        self._location = location
        self._islocked = locked
        self._inscene = inscene
        # :future: add a `cost` attribute
        pass


    def is_filepath_valid(self) -> bool:
        '''Checks if the `filepath` is an existing file and has a proper image 
        extension: `.jpg`, `.png`.'''
        f = self.get_filepath()
        exts = ['.jpg', '.png']
        return os.path.exists(f) and os.path.isfile(f) and \
            os.path.splitext(f)[1].lower() in exts


    # :todo: serialize into a `dict` + test
    def to_dict(self) -> dict:
        '''Serializes `Resource` object into json-compatible `dict`.'''
        pass


    # :todo: deserialize from a `dict` + test
    @classmethod
    def from_dict(cls, data: dict):
        '''Deserializes a `dict` loaded from json into a `Resource` object.'''
        pass


    def get_filepath(self) -> str:
        return self._filepath


    def get_location(self) -> Tuple[float, float]:
        return self._location


    def is_locked(self) -> bool:
        return self._islocked
    

    def is_inscene(self) -> bool:
        return self._inscene


    def set_filepath(self, f: str) -> None:
        self._filepath = f


    def set_location(self, l: Tuple[float, float]):
        self._location = l


    def set_islocked(self, l: bool):
        self._islocked = l


    def set_inscene(self, i: bool):
        self._inscene = i
    pass


class TestResource(unittest.TestCase): 
    def test_init(self):
        r = Resource("file", (1, 2), True, False)
        self.assertEqual("file", r._filepath)
        self.assertEqual((1, 2), r._location)
        self.assertEqual(True, r._islocked)
        self.assertEqual(False, r._inscene)
        pass

    # :todo: verify `to_dict` method works
    def test_to_dict(self):
        pass
    
    # :todo: verify `from_dict` method works
    def test_from_dict(self):
        pass


    def test_accessors_modifiers(self):
        r = Resource("file", (1, 2), True, False)
        self.assertEqual(r.get_location()[0], 1)
        self.assertEqual(r.get_location()[1], 2)
        self.assertEqual(r.get_filepath(), "file")
        self.assertEqual(r.is_inscene(), False)
        self.assertEqual(r.is_locked(), True)

        r.set_location((9.0, 42.3))
        self.assertEqual(r.get_location()[1], 42.3)
        self.assertEqual(r.get_location()[0], 9.0)

        r.set_islocked(False)
        self.assertEqual(r.is_locked(), False)

        r.set_inscene(True)
        self.assertEqual(r.is_inscene(), True)

        r.set_filepath("file2")
        self.assertEqual(r.get_filepath(), "file2")
        pass


    def test_filepath(self):
        r = Resource("", (1, 1), False, False)
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