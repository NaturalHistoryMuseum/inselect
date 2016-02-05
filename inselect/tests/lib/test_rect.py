import unittest

from inselect.lib.rect import Coordinates, Point, Rect


class TestCoordinates(unittest.TestCase):
    def test_comparison(self):
        self.assertEqual(Coordinates(1, 2, 3, 4), Coordinates(1, 2, 3, 4))
        self.assertNotEqual(Coordinates(1, 2, 3, 4), Coordinates(-1, 2, 3, 4))


class TestPoint(unittest.TestCase):
    def test_comparison(self):
        self.assertEqual(Point(1, 2), Point(1, 2))
        self.assertNotEqual(Point(1, 2), Point(-1, 2))


class TestRect(unittest.TestCase):
    R = Rect(0, 1, 2, 3)

    def test_rect(self):
        self.assertEqual(0, self.R.left)
        self.assertEqual(1, self.R.top)
        self.assertEqual(2, self.R.width)
        self.assertEqual(3, self.R.height)

    def test_iter(self):
        left, top, width, height = self.R
        self.assertEqual([0, 1, 2, 3], [left, top, width, height])

    def test_area(self):
        self.assertEqual(6, self.R.area)

    def test_coordinates(self):
        self.assertEqual(Coordinates(0, 1, 2, 4), self.R.coordinates)

    def test_topleft(self):
        self.assertEqual(Point(0, 1), self.R.topleft)

    def test_bottomright(self):
        self.assertEqual(Point(2, 4), self.R.bottomright)

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
            a == Point(1, 1)


if __name__ == '__main__':
    unittest.main()
