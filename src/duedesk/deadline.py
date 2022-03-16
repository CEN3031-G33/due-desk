# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : deadline
# Abstract : 
#   A deadline is a date-like object that can be compared against each other.
#   It can be parsed in multiple ways from a str.
# ------------------------------------------------------------------------------
import unittest
import json
from datetime import date

# :wip:
class Deadline:
    def __init__(self, year: int, month: int, day: int) -> None:
        '''Creates a new `Deadline` object.'''
        self._year = year
        self._month = month
        self._day = day
        pass


    @classmethod
    def from_str(cls, s: str):
        d = Deadline(date.today().year, date.today().month, date.today().day)
        delims = ['-', '/', '.', '\\']
        sep = None
        # auto-detect the delimiter
        for c in s:
            if c in delims:
                sep = c
                break
        parts = []
        # work backward from day to year
        parts = s.split(sep)
        parts.reverse()
        if len(parts) > 0:
            d.set_day(int(parts[0]))
        if len(parts) > 1:
            d.set_month(int(parts[1]))
        if len(parts) > 2:
            d.set_year(int(parts[2]))
        return d


    def days_out(self) -> int:
        '''Computes how many days from today until deadline.'''
        result = self.get_day() - date.today().day
        return result


    def __gt__(self, o) -> bool:
        if self.get_year() != o.get_year():
            return self.get_year() > o.get_year()
        elif self.get_month() != o.get_month():
            return self.get_month() > o.get_month()
        else:
            return self.get_day() > o.get_day()


    def __lt__(self, o) -> bool:
        return not (self > o)


    def __eq__(self, o) -> bool:
        return self.get_year() == o.get_year() and \
            self.get_month() == o.get_month() and \
            self.get_day() == o.get_day()


    def __ne__(self, o) -> bool:
        return not (self == o)


    def __le__(self, o) -> bool:
        return (self < o) or (self == o)


    def _ge__(self, o) -> bool:
        return (self > o) or (self == o)


    def get_year(self) -> int:
        return self._year


    def get_month(self) -> int:
        return self._month


    def get_day(self) -> int:
        return self._day


    def set_year(self, y: int) -> None:
        self._year = y


    def set_month(self, m: int) -> None:
        self._month = m


    def set_day(self, d: int) -> None:
        self._day = d
    pass


class TestDeadline(unittest.TestCase):
    def test_new(self):
        d = Deadline(2022, 1, 2)
        self.assertEqual(d.get_day(), 2)
        self.assertEqual(d.get_month(), 1)
        self.assertEqual(d.get_year(), 2022)
        pass

    def test_cmp(self):
        d0 = Deadline(2022, 1, 2)
        d1 = Deadline(2022, 1, 2)
        self.assertEqual(d0, d1)

        self.assertFalse(d0 > d1)
        self.assertFalse(d1 > d0)

        d2 = Deadline(2023, 1, 2)
        self.assertNotEqual(d2, d1)
        self.assertTrue(d2 > d1)
        self.assertFalse(d1 > d2)

        self.assertTrue(d1 < d2)
        self.assertFalse(d2 < d1)

        d2 = Deadline(2022, 2, 2)
        self.assertNotEqual(d2, d1)
        self.assertTrue(d2 > d1)
        self.assertFalse(d1 > d2)

        self.assertTrue(d1 < d2)
        self.assertFalse(d2 < d1)

        d2 = Deadline(2022, 1, 3)
        self.assertNotEqual(d2, d1)
        self.assertTrue(d2 > d1)
        self.assertFalse(d1 > d2)

        self.assertTrue(d1 < d2)
        self.assertFalse(d2 < d1)
        pass


    def test_from_str(self):
        self.assertEqual(Deadline.from_str('2022-01-02'), Deadline(2022, 1, 2))
        self.assertEqual(Deadline.from_str('2022/01/02'), Deadline(2022, 1, 2))
        self.assertEqual(Deadline.from_str('01/02'), Deadline(2022, 1, 2))
        pass


    def test_days_out(self):
        d = Deadline.from_str('3.18')
        self.assertEqual(d.days_out(), d.get_day() - date.today().day)

        d = Deadline.from_str('3.14')
        self.assertEqual(d.days_out(), d.get_day() - date.today().day)
        pass
    pass