# -*- coding: utf-8 -*-
import unittest

from datetime import date

from inselect.lib.parse import (parse_latitude, parse_int, parse_float,
                                parse_int_gt0, parse_float_gt0,
                                parse_four_digit_int, parse_one_or_two_digit_int,
                                parse_date, parse_sparse_date,
                                parse_latitude, parse_longitude,
                                assemble_dms)


class TestParse(unittest.TestCase):
    def test_int(self):
        # Empty
        self.assertIsNone(parse_int(''))
        self.assertIsNone(parse_int(' '))
        self.assertIsNone(parse_int(None))

        # Zero
        self.assertEqual(0, parse_int('0'))

        # Spaces
        self.assertEqual(1, parse_int('1'))
        self.assertEqual(1, parse_int(' 1 '))
        self.assertEqual(1, parse_int(' 1'))
        self.assertEqual(1, parse_int('1 '))

        # Negative
        self.assertEqual(-1, parse_int('-1'))
        self.assertEqual(-1, parse_int(' -1 '))
        self.assertEqual(-1, parse_int(' -1'))
        self.assertEqual(-1, parse_int('-1 '))

        # Leading zeroes
        self.assertEqual(10, parse_int(' 00010'))
        self.assertEqual(-10, parse_int('-00010 '))

        # Other values
        self.assertEqual(23, parse_int('  23  '))
        self.assertEqual(600001, parse_int('600001'))
        self.assertEqual(-1234567890, parse_int('-1234567890'))

        # Bad values
        self.assertRaises(ValueError, parse_int, 'a')
        self.assertRaises(ValueError, parse_int, '1.1')
        self.assertRaises(ValueError, parse_int, '1.0')
        self.assertRaises(ValueError, parse_int, '1.')

    def test_float(self):
        self.assertIsNone(parse_float(''))
        self.assertIsNone(parse_float(' '))
        self.assertIsNone(parse_float(None))

        self.assertEqual(0, parse_float('0'))

        # Integer
        self.assertEqual(1.0, parse_float('1'))
        self.assertEqual(1.0, parse_float(' 1'))
        self.assertEqual(1.0, parse_float('1 '))
        self.assertEqual(1.0, parse_float(' 1 '))

        # Float
        self.assertEqual(1.0, parse_float('1.0'))
        self.assertEqual(1.0, parse_float(' 1.0'))
        self.assertEqual(1.0, parse_float('1.0 '))
        self.assertEqual(1.0, parse_float(' 1.0 '))

        # More traling zeroes
        self.assertEqual(1.0, parse_float('1.00'))
        self.assertEqual(1.0, parse_float('1.0000000000'))

        # Fractional part
        self.assertEqual(1.1, parse_float('1.1'))
        self.assertEqual(1.1, parse_float('1.10'))

        # Negative numbers
        self.assertEqual(-1.1, parse_float('-1.1'))
        self.assertEqual(-1.1, parse_float('-1.10'))

        # Leading zeroes
        self.assertEqual(99, parse_float(' 0099  '))
        self.assertEqual(-1.1, parse_float('-001.1'))

        # Engineering form
        self.assertEqual(1e10, parse_float('1e10'))
        self.assertEqual(1e-10, parse_float('1e-10'))
        self.assertEqual(0.0, parse_float('0.0'))
        self.assertEqual(1e5, parse_float('1e5'))
        self.assertEqual(1e-5, parse_float('1e-5'))
        self.assertEqual(-1e-5, parse_float('-1e-5'))

        # Bad values
        self.assertRaises(ValueError, parse_float, '1.0.')
        self.assertRaises(ValueError, parse_float, 'e5')
        self.assertRaises(ValueError, parse_float, '1e')

    def test_parse_int_gt0(self):
        self.assertIsNone(parse_int_gt0(''))
        self.assertIsNone(parse_int_gt0(' '))
        self.assertIsNone(parse_int_gt0(None))

        self.assertEqual(1, parse_int_gt0('1'))
        self.assertEqual(2001, parse_int_gt0(' 2001   '))

        self.assertRaises(ValueError, parse_int_gt0, '0')
        self.assertRaises(ValueError, parse_int_gt0,'-10')

    def test_parse_float_gt0(self):
        self.assertIsNone(parse_float_gt0(''))
        self.assertIsNone(parse_float_gt0(' '))
        self.assertIsNone(parse_float_gt0(None))

        self.assertEqual(1.0, parse_float_gt0('1'))
        self.assertEqual(1.0, parse_float_gt0('1.0'))
        self.assertEqual(2001, parse_float_gt0(' 2001   '))
        self.assertEqual(2001.0, parse_float_gt0(' 2001   '))

        self.assertRaises(ValueError, parse_float_gt0, '0')
        self.assertRaises(ValueError, parse_float_gt0,'-10')

    def test_parse_date(self):
        self.assertIsNone(parse_date(''))
        self.assertIsNone(parse_date(' '))
        self.assertIsNone(parse_date(None))

        self.assertEqual(date(2012,8,1), parse_date('2012-08-01'))
        self.assertEqual(date(2012,8,1), parse_date('2012-8-1'))
        self.assertEqual(date(2012,8,1), parse_date(' 2012-8-1 '))

        self.assertRaises(ValueError, parse_date, '12-8-1')
        self.assertRaises(ValueError, parse_date, '12--1')
        self.assertRaises(ValueError, parse_date, '12-8-')
        self.assertRaises(ValueError, parse_date, '-8-1')

    def test_parse_sparse_date(self):
        # sparse_date delegates to assemble_sparse_date(), which has a more
        # comprehensive test plan.
        self.assertIsNone(parse_sparse_date(None, None, None))
        self.assertEqual( (2012,1,1),
                          tuple(parse_sparse_date('2012', '1', '1')))
        self.assertEqual( (2012,12,31),
                          tuple(parse_sparse_date('2012', '12', '31')))

        # February in a leap year
        self.assertEqual( (2012,2,29),
                         tuple(parse_sparse_date('2012', '2', '29')))

        # February in a non-leap year
        self.assertRaises(ValueError,
                          parse_sparse_date, '2011', '2', '29')

    def test_parse_four_digit_int(self):
        self.assertIsNone(parse_four_digit_int(''))
        self.assertIsNone(parse_four_digit_int(' '))
        self.assertIsNone(parse_four_digit_int(None))

        self.assertEqual(2001, parse_four_digit_int('2001'))
        self.assertEqual(2001, parse_four_digit_int(' 2001   '))

        self.assertRaises(ValueError, parse_four_digit_int, '1')
        self.assertRaises(ValueError, parse_four_digit_int, '-2001')
        self.assertRaises(ValueError, parse_four_digit_int, '20001')

    def test_parse_one_or_two_digit_int(self):
        self.assertIsNone(parse_one_or_two_digit_int(''))
        self.assertIsNone(parse_one_or_two_digit_int(' '))
        self.assertIsNone(parse_one_or_two_digit_int(None))

        self.assertEqual(1, parse_one_or_two_digit_int('1'))
        self.assertEqual(1, parse_one_or_two_digit_int('01'))
        self.assertEqual(31, parse_one_or_two_digit_int('31'))

        self.assertRaises(ValueError, parse_one_or_two_digit_int, '-2')
        self.assertRaises(ValueError, parse_one_or_two_digit_int,'123')


class TestParseDegrees(unittest.TestCase):
    def test_units_and_separators(self):
        self.assertEqual(-41.38, parse_latitude('-41.38'))
        self.assertEqual(-41.38, parse_latitude('41 22.8S'))
        self.assertEqual(-41.38, parse_latitude('41 22 48S'))
        self.assertAlmostEqual(-41.380008333333336, parse_latitude('41:22:48.03S'))
        self.assertEqual(-41.38, parse_latitude('41 22\' 48" S'))
        self.assertEqual(-41.38, parse_latitude('41 22\' 48\'\' S'))
        self.assertEqual(-41.38, parse_latitude(' 41°  22\'  48"  S  '))
        self.assertEqual(-41.38, parse_latitude('41°22\'48"S'))
        self.assertEqual(-41.38, parse_latitude('41°22′48″S'))

    def test_arithmetic(self):
        self.assertIsNone(parse_latitude(None))
        self.assertIsNone(parse_latitude(''))
        self.assertEqual( 1, parse_latitude('1'))
        self.assertEqual(-1, parse_latitude('-1'))
        self.assertEqual( 1, parse_latitude('1 n'))
        self.assertEqual(-1, parse_latitude('1 S '))
        self.assertAlmostEqual(1.5111111111111111,  parse_latitude('1 30 40 N'))
        self.assertAlmostEqual(1.5111111111111111,  parse_longitude('1 30 40 E'))
        self.assertAlmostEqual(-1.5111111111111111, parse_latitude('1 30 40 S'))
        self.assertAlmostEqual(-1.5111111111111111, parse_longitude('1 30 40 W'))
        self.assertAlmostEqual(89.99972222222222,   parse_latitude('89 59 59 N'))
        self.assertAlmostEqual(179.99972222,        parse_longitude('179 59 59 e'))
        self.assertAlmostEqual(-89.99972222222222,  parse_latitude('89 59 59 s'))
        self.assertAlmostEqual(-179.99972222,       parse_longitude('179 59 59 w'))

        # DMS values with floating-point minutes
        self.assertAlmostEqual(1.500185,            parse_latitude('1 30 0.666 N'))

        # DMS values with floating-point seconds
        self.assertEqual(1.0002777777777778,        parse_latitude('1 0 1 N'))
        self.assertAlmostEqual(1.5166666638888888,  parse_latitude('1 30 59.99999 N'))
        self.assertAlmostEqual(-179.99999999999721, parse_longitude('179 59 59.99999999 W'))

        # Zero degrees
        self.assertEqual(0.5,                             parse_latitude('0 30 0 N'))
        self.assertAlmostEqual(0.5083333333333333,        parse_latitude('0 30 30 N'))

        # All zeroes
        self.assertEqual(0, parse_latitude('0 0 0 N'))

    def test_bad_direction(self):
        self.assertRaises(ValueError, parse_latitude, 'E')
        self.assertRaises(ValueError, parse_latitude, '1 NS')
        self.assertRaises(ValueError, parse_latitude, '1 NE')
        self.assertRaises(ValueError, parse_latitude, '1 X')
        self.assertRaises(ValueError, parse_latitude, '1 2 X')
        self.assertRaises(ValueError, parse_latitude, '1 2 3 X')

    def test_bad_dms_components(self):
        self.assertRaises(ValueError, parse_latitude, '-1 N')        # -ve deg and direction
        self.assertRaises(ValueError, parse_latitude, '-1 S')        # -ve deg and direction
        self.assertRaises(ValueError, parse_longitude, '-1 E')       # -ve deg and direction
        self.assertRaises(ValueError, parse_longitude, '-1 W')       # -ve deg and direction
        self.assertRaises(ValueError, parse_latitude, '1 1')         # deg, min, no direction
        self.assertRaises(ValueError, parse_latitude, '1 1 1')       # deg, min, sec, no direction
        self.assertRaises(ValueError, parse_latitude, '-1 0 0 S')    # -ve deg and direction
        self.assertRaises(ValueError, parse_latitude, '0 -1 0 S')    # -ve minutes
        self.assertRaises(ValueError, parse_latitude, '0 60 0 S')    # minutes > 59
        self.assertRaises(ValueError, parse_latitude, '0 0 -1 S')    # -ve seconds
        self.assertRaises(ValueError, parse_latitude, '0 0 60 S')    # seconds > 59
        self.assertRaises(ValueError, parse_latitude, '91 N')        # Latitude > 90
        self.assertRaises(ValueError, parse_latitude, '91 S')        # Latitude < -90
        self.assertRaises(ValueError, parse_latitude, '90 1 0 N')    # Latitude > 90
        self.assertRaises(ValueError, parse_latitude, '90 1 1 N')    # Latitude > 90
        self.assertRaises(ValueError, parse_latitude, '90 1 1 S')    # Latitude < -90
        self.assertRaises(ValueError, parse_latitude, '90 1 1 S')    # Latitude < -90
        self.assertRaises(ValueError, parse_longitude, '181 E')      # Longitude > 180 
        self.assertRaises(ValueError, parse_longitude, '181 W')      # Longitude < -180
        self.assertRaises(ValueError, parse_longitude, '180 1 0 E')  # Longitude > 180
        self.assertRaises(ValueError, parse_longitude, '180 1 1 E')  # Longitude > 180
        self.assertRaises(ValueError, parse_longitude, '180 1 0 W')  # Longitude < -180
        self.assertRaises(ValueError, parse_longitude, '180 1 1 W')  # Longitude < -180
        self.assertRaises(ValueError, parse_latitude, '1 1 1 E')     # Incorrect direction
        self.assertRaises(ValueError, parse_latitude, '1 1 1 W')     # Incorrect direction
        self.assertRaises(ValueError, parse_longitude, '1 1 1 N')    # Incorrect direction
        self.assertRaises(ValueError, parse_longitude, '1 1 1 S')    # Incorrect direction
        self.assertRaises(ValueError, parse_latitude, '1 1\'\' S')   # Seconds without minutes
        self.assertRaises(ValueError, parse_latitude, '1 2 3 4 E')   # Too many numbers

    def test_bad_fractional_parts(self):
        # Seconds and fractional minutes
        self.assertRaises(ValueError, parse_latitude, '30 1.1 1 N')

    def test_assemble_dms_bad_direction(self):
        # There is one route through assemble_dms() that it is impossible to
        # reach via parse_latitude or parse_longitude
        self.assertRaises(ValueError, assemble_dms, 1, 1, 1, 'x', True)


if __name__=='__main__':
    unittest.main()
