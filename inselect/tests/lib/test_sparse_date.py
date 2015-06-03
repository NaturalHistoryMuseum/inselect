import datetime
import unittest

from inselect.lib.inselect_error import InselectError
from inselect.lib.sparse_date import SparseDate


class TestSparseDate(unittest.TestCase):
    def test_init(self):
        self.assertRaises(ValueError, SparseDate, None, None, None)
        self.assertEqual( (2012,1,1), tuple(SparseDate(2012, 1, 1)))
        self.assertEqual( (2012,12,31), tuple(SparseDate(2012, 12, 31)))

    def test_as_bool(self):
        self.assertTrue(SparseDate(2012, None, None))
        self.assertTrue(SparseDate(2012, 1, None))
        self.assertTrue(SparseDate(2012, 1, 2))

    def test_resolution(self):
        self.assertEqual( 'day', SparseDate(2012, 2, 29).resolution)
        self.assertEqual( 'month', SparseDate(2012, 2, None).resolution)
        self.assertEqual( 'year', SparseDate(2012, None, None).resolution)

    def test_illegal_dates(self):
        # February in a leap year
        self.assertEqual( (2012,2,29), tuple(SparseDate(2012, 2, 29)))

        # February in a non-leap year
        self.assertRaises(ValueError, SparseDate, 2011, 2, 29)

    def test_zero(self):
        # Zero year, month or day
        self.assertRaises(ValueError, SparseDate, 0000, None, None)
        self.assertRaises(ValueError, SparseDate, 2000, 0, None)
        self.assertRaises(ValueError, SparseDate, 2000, 1, 0)

    def test_invalid_month(self):
        self.assertRaises(ValueError, SparseDate, 2012, 0, 1)
        self.assertRaises(ValueError, SparseDate, 2012, -1, 1)
        self.assertRaises(ValueError, SparseDate, 2012, 13, 1)

    def test_invalid_day(self):
        self.assertRaises(ValueError, SparseDate, 2012, 1, -1)
        self.assertRaises(ValueError, SparseDate, 2012, 1, 32)

    def test_missing_year(self):
        self.assertRaises(ValueError, SparseDate, None, 1, None)
        self.assertRaises(ValueError, SparseDate, None, 1, 1)

    def test_missing_month(self):
        self.assertRaises(ValueError, SparseDate, 2012, None, 1)

    def test_noninteger_values(self):
        self.assertRaises(ValueError, SparseDate, 2012.0, None, None)
        self.assertRaises(ValueError, SparseDate, 2012, 1.0, None)
        self.assertRaises(ValueError, SparseDate, 2012, 1, 1.0)

    def test_downsample(self):
        self.assertEqual( SparseDate(2012, 5, 1).downsample('day'), SparseDate(2012, 5, 1) )
        self.assertEqual( SparseDate(2012, 5, 1).downsample('month'), SparseDate(2012, 5, None) )
        self.assertEqual( SparseDate(2012, 5, 1).downsample('year'), SparseDate(2012, None, None) )

        with self.assertRaises(ValueError):
            SparseDate(2012, 1, None).downsample('day')

        with self.assertRaises(ValueError):
            SparseDate(2012, None, None).downsample('month')

        with self.assertRaises(ValueError):
            SparseDate(2012, 1, None).downsample('x')

        with self.assertRaises(ValueError):
            SparseDate(2012, 1, None).downsample('')

    def test_downsample_to_common(self):
        a  = SparseDate(2012, 6, 1)
        self.assertEqual([SparseDate(2012, 6, 1)],
                         list(SparseDate.downsample_to_common( [a] )))

        b  = SparseDate(2012, 1, None)
        self.assertEqual([SparseDate(2012, 6, None), SparseDate(2012, 1, None)],
                         list(SparseDate.downsample_to_common( [a,b] )))

        c = SparseDate(2012, None, None)
        self.assertEqual([SparseDate(2012, None, None),
                          SparseDate(2012, None, None),
                          SparseDate(2012, None, None)],
                         list(SparseDate.downsample_to_common( [a,b,c] )))

    def test_comparison(self):
        # Equal
        self.assertEqual( SparseDate(2012,None,None), SparseDate(2012,None,None) )
        self.assertEqual( SparseDate(2012,1,None), SparseDate(2012,1,None) )
        self.assertEqual( SparseDate(2012,1,1), SparseDate(2012,1,1) )

        # Not equal
        self.assertNotEqual( SparseDate(2012,None,None), SparseDate(2011,None,None) )
        self.assertNotEqual( SparseDate(2012,1,None), SparseDate(2012,2,None) )
        self.assertNotEqual( SparseDate(2012,1,1), SparseDate(2012,1,2) )

        # Greater
        self.assertGreater( SparseDate(2013,None,None), SparseDate(2012,None,None) )
        self.assertGreaterEqual( SparseDate(2012,None,None), SparseDate(2012,None,None) )
        self.assertGreaterEqual( SparseDate(2013,None,None), SparseDate(2012,None,None) )
        self.assertGreater( SparseDate(2012,2,None), SparseDate(2012,1,None) )
        self.assertGreaterEqual( SparseDate(2012,1,None), SparseDate(2012,1,None) )
        self.assertGreaterEqual( SparseDate(2012,2,None), SparseDate(2012,1,None) )
        self.assertGreater( SparseDate(2012,1,2), SparseDate(2012,1,1) )
        self.assertGreaterEqual( SparseDate(2012,1,1), SparseDate(2012,1,1) )
        self.assertGreaterEqual( SparseDate(2012,1,2), SparseDate(2012,1,1) )

        # Less
        self.assertLess( SparseDate(2012,None,None), SparseDate(2013,None,None) )
        self.assertLessEqual( SparseDate(2012,None,None), SparseDate(2012,None,None) )
        self.assertLessEqual( SparseDate(2012,None,None), SparseDate(2013,None,None) )
        self.assertLess( SparseDate(2012,1,None), SparseDate(2012,2,None) )
        self.assertLessEqual( SparseDate(2012,1,None), SparseDate(2012,1,None) )
        self.assertLessEqual( SparseDate(2012,1,None), SparseDate(2012,2,None) )
        self.assertLess( SparseDate(2012,1,1), SparseDate(2012,1,2) )
        self.assertLessEqual( SparseDate(2012,1,1), SparseDate(2012,1,1) )
        self.assertLessEqual( SparseDate(2012,1,1), SparseDate(2012,1,2) )

        # Can't compare SparseDates of different resolutions
        with self.assertRaises(InselectError):
            SparseDate(2012, None, None) > SparseDate(2012, 1, None)
        with self.assertRaises(InselectError):
            SparseDate(2012, 1, None) > SparseDate(2012, 1, 1)

        a = SparseDate(2012, 1, None)
        with self.assertRaises(NotImplementedError):
            a == ''
        with self.assertRaises(NotImplementedError):
            a == 1
        with self.assertRaises(NotImplementedError):
            a == None

    def test_range(self):
        self.assertEqual( SparseDate(2012,1,1), SparseDate(2012,None,None).earliest() )
        self.assertEqual( SparseDate(2012,12,31), SparseDate(2012,None,None).latest() )

        self.assertEqual( SparseDate(2012,2,1), SparseDate(2012,2,None).earliest() )
        self.assertEqual( SparseDate(2012,2,29), SparseDate(2012,2,None).latest() )

        self.assertEqual( SparseDate(2012,2,5), SparseDate(2012,2,5).earliest() )
        self.assertEqual( SparseDate(2012,2,5), SparseDate(2012,2,5).latest() )

    def test_as_date(self):
        self.assertEqual( datetime.date(2012,8,1), SparseDate(2012,8,1).as_date())
        with self.assertRaises(InselectError):
            SparseDate(2012,8,None).as_date()

    def test_hash(self):
        a,b,c = SparseDate(2012,8,1), SparseDate(2012,8,None), SparseDate(2012,None,None)

        self.assertEqual(hash(a), hash(SparseDate(2012,8,1)))
        self.assertNotEqual(hash(a), hash(b))
        self.assertNotEqual(hash(a), hash(c))
        self.assertNotEqual(hash(b), hash(c))

    def test_str(self):
        a,b,c = SparseDate(2012,8,1), SparseDate(2012,8,None), SparseDate(2012,None,None)

        self.assertEqual('2012-8-1', str(a))
        self.assertEqual('2012-8-None', str(b))
        self.assertEqual('2012-None-None', str(c))

        self.assertEqual(eval(repr(a)), a)
        self.assertEqual(eval(repr(b)), b)
        self.assertEqual(eval(repr(c)), c)


if __name__=='__main__':
    unittest.main()
