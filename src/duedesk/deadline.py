# ------------------------------------------------------------------------------
# Project  : DueDesk
# Module   : deadline
# Abstract : 
#   A deadline is a date-like object that can be compared against each other.
#   It can be parsed in multiple ways from a str.
# ------------------------------------------------------------------------------
import unittest
from datetime import date
from calendar import monthrange

class Deadline:
    def __init__(self, year: int, month: int, day: int) -> None:
        '''Creates a new `Deadline` object.'''
        self._year = year
        self._month = month
        self._day = day
        pass


    @classmethod
    def from_str(cls, s: str):
        '''Transforms a `str` into a `Deadline` object. Note: this method can
        fail. To check if a valid `Deadline` was created, call `is_valid()`.'''
        d = Deadline(date.today().year, date.today().month, date.today().day)
        delims = ['-', '/', '.', '\\']
        sep = delims[0]
        # auto-detect the delimiter
        for c in s:
            if c in delims:
                sep = c
                break
        parts = []
        # work backward from day to year
        parts = s.split(sep)
        parts.reverse()
        # too many parts
        if len(parts) > 3:
            return Deadline(0, 0, 0)
        # accept days then months then years
        if len(parts) > 0:
            try:
                d.set_day(int(parts[0]))
            except:
                d.set_day(0)
        if len(parts) > 1:
            try:
                d.set_month(int(parts[1]))
            except:
                d.set_month(0)
        if len(parts) > 2:
            try:
                d.set_year(int(parts[2]))
            except:
                d.set_year(0)
        # verify month and day are within correct ranges
        if d.get_month() > 12:
            d.set_month(0)
        if d.get_year() != 0 and d.get_month() != 0 and \
            d.get_day() > monthrange(d.get_year(), d.get_month())[1]:
            d.set_day(0)
        return d


    def days_out(self) -> int:
        '''Computes how many days from today until deadline.'''
        result = (date(self.get_year(), self.get_month(), self.get_day()) - date.today()).days
        return result


    def is_valid(self) -> bool:
        '''Checks if the current date is valid. Invalid dates are signified
        with the caught position set to 0.'''
        return self.get_day() != 0 and \
            self.get_month() != 0 and \
            self.get_year() != 0


    def is_overdue(self) -> bool:
        return self.days_out() < 0


    def __str__(self) -> str:
        '''Convert the `deadline` to a str.'''
        return str(self.get_year()).zfill(4)+'-'+str(self.get_month()).zfill(2)+'-'+str(self.get_day()).zfill(2)


    def __gt__(self, o) -> bool:
        if self.get_year() != o.get_year():
            return self.get_year() > o.get_year()
        elif self.get_month() != o.get_month():
            return self.get_month() > o.get_month()
        else:
            return self.get_day() > o.get_day()


    def __lt__(self, o) -> bool:
        if self.get_year() != o.get_year():
            return self.get_year() < o.get_year()
        elif self.get_month() != o.get_month():
            return self.get_month() < o.get_month()
        else:
            return self.get_day() < o.get_day()


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


    def __repr__(self) -> str:
        return str(id(self))+': '+str(self)
    pass


class TestDeadline(unittest.TestCase):
    def test_new(self):
        d = Deadline(2022, 1, 2)
        self.assertEqual(d.get_day(), 2)
        self.assertEqual(d.get_month(), 1)
        self.assertEqual(d.get_year(), 2022)
        pass


    def test_from_str(self):
        # valid cases
        self.assertEqual(Deadline.from_str('2022-01-02'), Deadline(2022, 1, 2))
        self.assertEqual(Deadline.from_str('2022/01/02'), Deadline(2022, 1, 2))
        self.assertEqual(Deadline.from_str('01/02'), Deadline(2022, 1, 2))
        self.assertEqual(Deadline.from_str('200\\1\\02'), Deadline(200, 1, 2))
        # invalid formatting cases
        self.assertEqual(Deadline.from_str('-2022/04/02').is_valid(), False)
        self.assertEqual(Deadline.from_str('2022-04/02').is_valid(), False)
        self.assertEqual(Deadline.from_str('abc/04/02').is_valid(), False)
        self.assertEqual(Deadline.from_str('-4').is_valid(), False)
        self.assertEqual(Deadline.from_str('2022/04.02').is_valid(), False)
        self.assertEqual(Deadline.from_str(''), Deadline(date.today().year, date.today().month, 0))
        # month out of range cases
        self.assertEqual(Deadline.from_str('2022/13/02').is_valid(), False)
        # days out of range cases
        self.assertEqual(Deadline.from_str('2022/2/29').is_valid(), False)
        self.assertEqual(Deadline.from_str('2022/5/32').is_valid(), False)
        pass


    def test_days_out(self):
        d = Deadline.from_str('3.25')
        self.assertEqual(d.days_out(), (date(d.get_year(), d.get_month(), d.get_day()) - date.today()).days)

        d = Deadline.from_str('8.12')
        self.assertEqual(d.days_out(), (date(d.get_year(), d.get_month(), d.get_day()) - date.today()).days)
        pass

    def test_overdue(self):
        d0 = Deadline(2022, 1, 1)
        d1 = Deadline(2030, 1, 1)
        self.assertTrue(d0.is_overdue())
        self.assertFalse(d1.is_overdue())


    def test_to_str(self):
        d = Deadline(2022, 1, 5)
        self.assertEqual(str(d), '2022-01-05')
        d = Deadline(200, 10, 28)
        self.assertEqual(str(d), '0200-10-28')
        d = Deadline(2022, 12, 12)
        self.assertEqual(str(d), '2022-12-12')
        pass


    def test_is_valid(self):
        # invalid everything
        d = Deadline(0, 0, 0)
        self.assertFalse(d.is_valid())
        # invalid year
        d = Deadline(0, 12, 1)
        self.assertFalse(d.is_valid())
        # invalid month
        d = Deadline(2022, 0, 1)
        self.assertFalse(d.is_valid())
        # invalid day
        d = Deadline(2022, 4, 0)
        self.assertFalse(d.is_valid())
        # valid deadline
        d = Deadline(2022, 1, 1)
        self.assertTrue(d.is_valid())
        pass


    def test_cmp(self):
        # equal deadlines
        d0 = Deadline(2022, 1, 2)
        d1 = Deadline(2022, 1, 2)
        self.assertEqual(d0, d1)
        self.assertFalse(d0 != d1)

        self.assertFalse(d0 > d1)
        self.assertFalse(d1 > d0)
        self.assertFalse(d1 < d0)
        self.assertFalse(d0 < d1)

        # future year
        d0 = Deadline(2023, 1, 2)
        self.assertNotEqual(d0, d1)
        self.assertFalse(d0 < d1)
        self.assertFalse(d1 > d0)

        self.assertTrue(d1 < d0)
        self.assertTrue(d0 > d1)

        # future month
        d0 = Deadline(2022, 2, 2)
        self.assertNotEqual(d0, d1)
        self.assertFalse(d1 > d0)
        self.assertFalse(d0 < d1)

        self.assertTrue(d0 > d1)
        self.assertTrue(d1 < d0)

        # future day
        d0 = Deadline(2022, 1, 3)
        self.assertNotEqual(d0, d1)
        self.assertFalse(d1 > d0)
        self.assertFalse(d0 < d1)

        self.assertTrue(d0 > d1)
        self.assertTrue(d1 < d0)
        pass
    pass