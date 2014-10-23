import unittest

from inselect.lib.rect import Coordinates, Point, Rect
from inselect.lib.inselect_error import InselectError


class TestCoordinates(unittest.TestCase):
    def test_comparison(self):
        self.assertEqual(Coordinates(1,2,3,4), Coordinates(1,2,3,4))
        self.assertNotEqual(Coordinates(1,2,3,4), Coordinates(-1,2,3,4))


class TestPoint(unittest.TestCase):
    def test_comparison(self):
        self.assertEqual(Point(1,2), Point(1,2))
        self.assertNotEqual(Point(1,2), Point(-1,2))


class TestRect(unittest.TestCase):
    R = Rect(0, 1, 2, 3)

    def test_rect(self):
        self.assertEqual(0, self.R.left)
        self.assertEqual(1, self.R.top)
        self.assertEqual(2, self.R.width)
        self.assertEqual(3, self.R.height)
        self.assertRaises(InselectError, Rect,-1, 1, 2, 3)
        self.assertRaises(InselectError, Rect, 0,-1, 2, 3)
        self.assertRaises(InselectError, Rect, 0, 1, 0, 3)
        self.assertRaises(InselectError, Rect, 0, 1, 2, 0)

    def test_str(self):
        self.assertEqual('0, 1, 2, 3 (Area 6)', str(self.R))

    def test_repr(self):
        self.assertEqual('Rect(0, 1, 2, 3)', repr(self.R))

    def test_iter(self):
        self.assertEqual([0, 1, 2, 3], list(self.R))

    def test_area(self):
        self.assertEqual(6, self.R.area)

    def test_coordinates(self):
        self.assertEqual(Coordinates(0, 1, 2, 4), self.R.coordinates)

    def test_centre(self):
        self.assertEqual(Point(1, 2), self.R.centre)

    def test_comparison(self):
        a = Rect(0, 1, 2, 3)
        self.assertEqual(a, self.R)
        b = Rect(9, 1, 2, 3)
        self.assertNotEqual(b, self.R)

        with self.assertRaises(NotImplementedError):
            a == ''

        with self.assertRaises(NotImplementedError):
            a == Point(1,1)


if __name__=='__main__':
    unittest.main()
