# -*- coding: utf-8 -*-
import inspect
import re
import sys

from datetime import date


from inselect.lib.sparse_date import SparseDate


# A dict {name: parse function}. Populated at the bottom of this file.
# All parse functions take a single argument called value. They raise a
# ValueError if value cannot be parsed, otherwise they return a single value.
PARSERS = {}

# Private regular expressions used by parse functions
_TWO_DIGITS_RE = re.compile(r'^\s*[0-9]{1,2}\s*$')
_FOUR_DIGITS_RE = re.compile(r'^\s*[0-9]{4}\s*$')

# YYYY-M[M]-D[D]
_DATE_YMD_RE = re.compile(r'^\s*([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})\s*$')

# One of
#   YYYY
#   YYYY-M[M]
#   YYYY-M[M]-D[D]
_SPARSEDATE_RE = re.compile(
    r'^\s*'
    r'([0-9]{4})'
    r'(?:-([0-9]{1,2})(?:-([0-9]{1,2}))?)?'
    r'\s*$'
)

# Degrees latitude or longitude. Re strings are unicode in order to match
# degrees symbol (°)
_DEGREES_RE = re.compile(
    r'^\s*'
    r'(?P<degrees>-?\d+(?:\.\d+)?)\s*[\sd°:]?\s*'
    r'(?:(?:(?P<minutes>\d+(?:\.\d+)?)\s*[\s\'′:]?\s*)?'
    r'(?:(?P<seconds>\d+(?:\.\d+)?)\s*(?:(?:[\s"″])|(?:\'\'))?\s*)?)?'
    r'(?P<direction>[NnSsEeWw]?)'
    r'\s*$', flags=re.UNICODE
)


def parse_int(value):
    """Returns value converted to an int. Raises a ValueError if value cannot
    be converted to an int.
    """
    return int(value)


def parse_float(value):
    """Returns value converted to a float. Raises a ValueError if value cannot
    be converted to a float.
    """
    return float(value)


def parse_int_gt0(value):
    """Returns value converted to an int. Raises a ValueError if value cannot
    be converted to an int that is greater than zero.
    """
    value = int(value)
    if value <= 0:
        msg = 'Invalid value [{0}]: require a whole number greater than zero'
        raise ValueError(msg.format(value))
    else:
        return value


def parse_int_ge0(value):
    """Returns value converted to an int. Raises a ValueError if value cannot
    be converted to an int that is greater than or equal to zero.
    """
    value = int(value)
    if value < 0:
        msg = ('Invalid value [{0}]: require a whole number greater than or '
               'equal to zero')
        raise ValueError(msg.format(value))
    else:
        return value


def parse_float_gt0(value):
    """Returns value converted to a float. Raises a ValueError if value cannot
    be converted to a float that is greater than zero.
    """
    value = float(value)
    if value <= 0:
        msg = 'Invalid value [{0}]: require a number greater than zero'
        raise ValueError(msg.format(value))
    else:
        return value


def parse_float_ge0(value):
    """Returns value converted to a float. Raises a ValueError if value cannot
    be converted to a float that is greater than or equal to zero.
    """
    value = float(value)
    if value < 0:
        msg = ('Invalid value [{0}]: require a number greater than or equal to '
               'zero')
        raise ValueError(msg.format(value))
    else:
        return value


def parse_sparse_date(value):
    """Returns a SparseDate. A ValueError is raised if value is not a string
    in one of the forms:
        YYYY
        YYYY-M[M]
        YYYY-M[M]-D[D]
    """
    match = _SPARSEDATE_RE.match(value)
    if match:
        year, month, day = match.groups()
        year = int(year)
        month = int(month) if month else None
        day = int(day) if day else None
        return SparseDate(year, month, day)
    else:
        msg = ('Badly formatted value [{0}]: require a sparse date in the '
               "form 'YYYY', 'YYYY-M[M]' or 'YYYY-M[M]-D[D]'")
        raise ValueError(msg.format(value))


def parse_four_digit_int(value):
    """Returns value converted to an int. Raises a ValueError if value is not a
    string with exactly four digits.
    """
    match = _FOUR_DIGITS_RE.match(value)
    if match:
        return int(match.group(0))
    else:
        msg = ('Badly formatted value [{0}]: require a four digit '
               'whole number')
        raise ValueError(msg.format(value))


def parse_one_or_two_digit_int(value):
    """Returns value converted to an int. Raises a ValueError if value is not
    a string with either one or two digits.
    """
    match = _TWO_DIGITS_RE.match(value)
    if match:
        return int(match.group(0))
    else:
        msg = ('Badly formatted value [{0}]: require a one or two digit '
               'whole number')
        raise ValueError(msg.format(value))


def parse_date(value):
    """Returns a datetime.date. Raises a ValueError if value is not a string
    in the form YYYY-M[M]-D[D].
    """
    match = _DATE_YMD_RE.match(value)
    if match:
        year, month, day = match.groups()
        return date(int(year), int(month), int(day))
    else:
        msg = ('Badly formatted value [{0}]: require a date '
               'in the form YYYY-MM-DD')
        raise ValueError(msg.format(value))


def parse_latitude(value):
    """Returns a float. Raises a ValueError if value is not a string that
    represents a latitude.
    """
    return _parse_degrees(value, True)


def parse_longitude(value):
    """Returns a float. Raises a ValueError if value is not a string that
    represents a longitude.
    """
    return _parse_degrees(value, False)


def _parse_degrees(value, is_latitude):
    """Returns a float. Raises a ValueError if value is not a string that
    represents an angle in degrees. is_latitude should be either True or False.
    """
    match = _DEGREES_RE.match(value)
    if match:
        deg, min, sec, dir = match.groups()
        deg = float(deg)
        min = float(min) if min else None
        sec = float(sec) if sec else None
        dir = dir if dir else None
        return _assemble_dms(deg, min, sec, dir, is_latitude)
    else:
        msg = 'Badly formatted DD MM SS value [{0}]'
        raise ValueError(msg.format(value))


def _assemble_dms(degrees, minutes, seconds, direction, is_latitude):
    """Returns a floating-point value of degrees of arc, computed from
    (degrees + minutes/60 + seconds/3600) x direction.

    degrees should be a float.
    minutes and seconds should be floats or None.

    is_latitude should be a bool.

    A ValueError is raised if any of the following is True:
        degrees < 0.0 and direction
        minutes and not direction
        seconds and minutes is None
        is_latitude is True and direction is None or is not in ('N', 'n', 'S', 's')
        is_latitude is False and direction is None or is not in ('E', 'e', 'W', 'w')
        minutes and not 0.0<=minutes<60.0
        seconds and not 0.0<=seconds<60.0
        is_latitude is True and for computed value, v, not   -90.0 <= v <=  90.0
        is_latitude is False and for computed value, v, not -180.0 <= v <= 180.0
    """

    direction = direction.lower() if direction else None
    if direction:
        if direction not in ('n', 's', 'e', 'w'):
            msg = 'Unexpected direction [{0}]'
            raise ValueError(msg.format(direction))
        elif direction in ('e', 'w'):
            dir_is_latitude = False
            negate = 'w' == direction
        elif direction in ('n', 's'):
            dir_is_latitude = True
            negate = 's' == direction
    else:
        # No direction given
        negate = False

    # Checks
    if degrees < 0.0 and direction:
        raise ValueError('Negative degrees with direction')
    elif minutes and not direction:
        raise ValueError('Minutes without direction')
    elif seconds and minutes is None:
        raise ValueError('Seconds without minutes')
    elif direction and dir_is_latitude != is_latitude:
        raise ValueError('Direction mismatch.')
    elif minutes and not float(minutes).is_integer() and seconds:
        msg = 'Both seconds [{0}] and fractional minutes [{1}] given'
        raise ValueError(msg.format(seconds, minutes))
    elif minutes and not 0.0 <= minutes < 60.0:
        msg = 'Bad minutes [{0}]. Require a number between 0 and 60'
        raise ValueError(msg.format(minutes))
    elif seconds and not 0.0 <= seconds < 60.0:
        msg = 'Bad seconds [{0}]. Require a number between 0 and 60'
        raise ValueError(msg.format(seconds))
    else:
        # Compute the floating-point degrees of arc
        degrees += minutes / 60.0 if minutes else 0.0
        degrees += seconds / 3600.0 if seconds else 0.0

        degrees *= -1.0 if negate else 1.0

        # Check bounds
        if not is_latitude and not -180 <= degrees <= 180:
            msg = 'Longitude [{0}] is outside of the range -180 to 180'
            raise ValueError(msg.format(degrees))
        elif is_latitude and not -90 <= degrees <= 90:
            msg = 'Computed latitude [{0}] is outside of the range -90 to 90'
            raise ValueError(msg.format(degrees))
        else:
            return degrees


def parse_matches_regex(regex, value, error_message='Unmatched value [{0}]'):
    """Raises ValueError(error_message) if value does not match regex.
    """
    res = regex.match(value)
    if not res:
        raise ValueError(error_message.format(value))
    else:
        return value


def parse_in_choices(choices, value):
    """Raise ValueError(error_message) if value is not in choices
    """
    if value not in choices:
        raise ValueError('Invalid value [{0}]: not in choices'.format(value))
    else:
        return value

# Populate dict {name: parse function}.
PARSERS = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
PARSERS = filter(lambda v: re.match(r'^parse_.+$', v[0]), PARSERS)
PARSERS = filter(lambda v: ['value'] == inspect.getargspec(v[1]).args, PARSERS)
PARSERS = dict(PARSERS)
