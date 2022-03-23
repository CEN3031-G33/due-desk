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
from typing import Tuple
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

    @classmethod
    def from_dict(cls, data: dict):
        '''Deserializes a `dict` loaded from json into a `Tasklist` object.'''
        resources = []
        for v in data.values():
            resources += [Resource.from_dict(v)]
        rp = Resourcepool(resources)
        return rp


    def to_dict(self) -> dict:
        '''Serializes `Tasklist` object into json-compatible `dict`.'''
        data = {}
        for r in enumerate(self._inner):
            data[str(r[0])] = r[1].to_dict()
        return data

    def filter_dups(self) -> None:
        '''Remove duplicate resources from list'''
        rpmap = {}
        for v in self._inner:
            if v.get_filepath().lower() not in rpmap.keys():
                rpmap[v.get_filepath().lower()] = v
        self._inner = list(rpmap.values())

    # :idea: create offset attribute if unique resource pixelmaps are implemented
    def get_by_location(self, location: Tuple[float, float]) -> Resource:
        '''Returns resource when mouse is clicked on resource pixelmap, returns None otherwise'''
        offset = 64.0
        for r in self._inner:
            if location[0] >= r.get_location()[0] and \
                location[0] <= r.get_location()[0] + offset and \
                location[1] >= r.get_location()[1] and \
                location[1] <= r.get_location()[1] + offset:
                    return r
        return None
        


    def __eq__(self, o) -> bool:
        '''Performs in-order element-wise partial equality check on `Resources`.'''
        if len(self._inner) != len(o._inner):
            return False
        else:
            for i in range(0, len(self._inner)):
                if not self._inner[i].partial_eq(o._inner[i]):
                    return False
        return True
    pass

class TestResourcelist(unittest.TestCase):
    def test_new_and_get_by_index(self):
        rp = Resourcepool([
            Resource("file", (1, 2), True, False, 3),
            Resource("./README.md", (1, 2), True, False, 3),
            Resource("./docs/images/superdesk.png", (1, 2), True, False, 3)
            ])

    def test_to_dict(self):
        rp = Resourcepool([
            Resource("file", (1.2, 5.4), True, False, 3),
            Resource("./README.md", (1.1, 2.0), True, False, -3),
            Resource("./docs/images/superdesk.png", (1, 2), False, True, 3)
            ])
        self.assertEqual(rp.to_dict(), 
        {
            "0": {
                "path": "file",
                "pixelmap": "(1.2, 5.4)",
                "locked": 'True',
                "inscene": "False",
                "cost": "3"
            },
            "1": {
                "path": "./README.md",
                "pixelmap": "(1.1, 2.0)",
                "locked": 'True',
                "inscene": "False",
                "cost": "0"
            },
            "2": {
                "path": "./docs/images/superdesk.png",
                "pixelmap": "(1, 2)",
                "locked": 'False',
                "inscene": "True",
                "cost": "3"
            }
        })
        pass


    def test_from_dict(self):
        data = {
            "0": {
                "path": "file",
                "pixelmap": "(1.2, 5.4)",
                "locked": 'True',
                "inscene": "False",
                "cost": "3"
            },
            "1": {
                "path": "./README.md",
                "pixelmap": "(1.1, 2.0)",
                "locked": 'True',
                "inscene": "False",
                "cost": "0"
            },
            "2": {
                "path": "./docs/images/superdesk.png",
                "pixelmap": "(1, 2)",
                "locked": 'False',
                "inscene": "True",
                "cost": "3"
            },
            "3": {
                "path": "./docs/images/superdesk.png",
                "pixelmap": "(1.1, 2.5)",
                "locked": 'True',
                "inscene": "False",
                "cost": "-2"
            }
        }
        self.assertEqual(Resourcepool.from_dict(data), Resourcepool([
            Resource("file", (1.2, 5.4), True, False, 3),
            Resource("./README.md", (1.1, 2.0), True, False, -3),
            Resource("./docs/images/superdesk.png", (1, 2), False, True, 3),
            Resource("./docs/images/superdesk.png", (1.1, 2.5), True, False, -2)
            ]))
        pass

    def test_remove_dups(self):
        rp0 = Resourcepool([
            Resource("file", (1.2, 5.4), True, False, 3),
            Resource("./README.md", (1.1, 2.0), True, False, -3),
            Resource("./docs/images/superdesk.png", (1, 2), False, True, 3),
            Resource("./docs/images/superdesk.png", (1.1, 2.5), True, False, -2)
            ])
        rp1 = Resourcepool([
            Resource("file", (1.2, 5.4), True, False, 3),
            Resource("./README.md", (1.1, 2.0), True, False, -3),
            Resource("./docs/images/superdesk.png", (1, 2), False, True, 3),
            ])
        rp0.filter_dups()
        self.assertEqual(rp0, rp1)

    def test_get_by_location(self):
        rp = Resourcepool([
            Resource("file", (10, 20.1), True, False, 3),
            Resource("./README.md", (50, 80), True, False, -3),
            Resource("./docs/images/superdesk.png", (17.4, 17.4), False, True, 3),
            ])
        self.assertEqual(rp.get_by_location((0.0, 0.0)), None)
        self.assertEqual(rp.get_by_location((10.0, 20.1)), rp.get_by_index(0))
        self.assertEqual(rp.get_by_location((113.9, 143.9)), rp.get_by_index(1))
        self.assertEqual(rp.get_by_location((114, 144)), rp.get_by_index(1))
        self.assertEqual(rp.get_by_location((114.1, 144)), None)
        self.assertEqual(rp.get_by_location((114, 144.1)), None)
