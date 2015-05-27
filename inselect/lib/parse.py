# -*- coding: utf-8 -*-
import re

from datetime import date

from .sparse_date import SparseDate


DATE_YMD_RE = re.compile(r'^\s*([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})\s*$')
DEGREES_RE = re.compile(ur'^\s*'
                        ur'(?P<degrees>-?\d+(?:\.\d+)?)\s*[\sd°:]?\s*'
                        ur"(?:(?:(?P<minutes>\d+(?:\.\d+)?)\s*[\s'′:]?\s*)?"
                        ur"(?:(?P<seconds>\d+(?:\.\d+)?)\s*(?:(?:[\s\"″])|(?:''))?\s*)?)?"
                        ur'(?P<direction>[NnSsEeWw]?)'
                        ur'\s*$', flags=re.UNICODE)

def parse_int_gt0(value):
    """Returns an int that is greater than zero
    """
    value = int(value)
    if value <= 0:
        msg = u'Invalid value [{0}]: require a whole number greater than zero'
        raise ValueError(msg.format(value))
    else:
        return value

def parse_int_ge0(value):
    """Returns an int that is greater than or equal to zero
    """
    value = int(value)
    if value < 0:
        msg = (u'Invalid value [{0}]: require a whole number greater than or '
               u'equal to zero')
        raise ValueError(msg.format(value))
    else:
        return value

def parse_float_gt0(value):
    """Returns a float that is greater than zero
    """
    value = float(value)
    if value <= 0:
        msg = u'Invalid value [{0}]: require a number greater than zero'
        raise ValueError(msg.format(value))
    else:
        return value

def parse_float_ge0(value):
    """Returns a float that is greater than or equal to zero
    """
    value = float(value)
    if value < 0:
        msg = (u'Invalid value [{0}]: require a number greater than or equal to '
               u'zero')
        raise ValueError(msg.format(value))
    else:
        return value

def parse_sparse_date(year, month, day):
    """Returns a SparseDate.
    Year should be a string of four digits or None. month and day should be
    strings of one or two digits or None.
    """
    year = parse_four_digit_int(year)
    month = parse_one_or_two_digit_int(month)
    day = parse_one_or_two_digit_int(day)
    if year:
        return SparseDate(year,
                          month if month else None,
                          day if day else None)
    else:
        raise ValueError(u'Invalid values [{0}] [{1}] [{2}]'.format(value))

def parse_four_digit_int(value):
    """Returns an int or None. Value should be a string of four digits or
    None.
    """
    match = re.match(r'^\s*[0-9]{4}\s*$', value)
    if match:
        return int(match.group(0))
    else:
        msg = (u'Badly formatted value [{0}]: require a four digit '
               u'whole number')
        raise ValueError(msg.format(value))

def parse_one_or_two_digit_int(value):
    """Returns an int or None. Value should be a string of one or two
    digits or None.
    """
    match = re.match(r'^\s*[0-9]{1,2}\s*$', value)
    if match:
        return int(match.group(0))
    else:
        msg = (u'Badly formatted value [{0}]: require a one or two digit '
               u'whole number')
        raise ValueError(msg.format(value))

def parse_date(value):
    """Returns a datetime.date. Value should be a string in the form
    YYYY-[M]M-[D]D.
    """
    match = DATE_YMD_RE.match(value)
    if match:
        year, month, day = match.groups()
        return date(int(year), int(month), int(day))
    else:
        msg = (u'Badly formatted value [{0}]: require a date '
               u'in the form YYYY-MM-DD')
        raise ValueError(msg.format(value))

def parse_latitude(value):
    return parse_degrees(value, True)

def parse_longitude(value):
    return parse_degrees(value, False)

def parse_degrees(value, is_latitude):
    """value should be a string. is_latitude should be either True or False
    Returns a floating-point degrees.
    """
    match = DEGREES_RE.match(value)
    if match:
        deg, min, sec, dir = match.groups()
        deg = float(deg)
        min = float(min) if min else None
        sec = float(sec) if sec else None
        dir = dir if dir else None
        return assemble_dms(deg, min, sec, dir, is_latitude)
    else:
        msg = u'Badly formatted d:m:s value [{0}]'
        raise ValueError(msg.format(value))

def assemble_dms(degrees, minutes, seconds, direction, is_latitude):
    """Returns a floating-point value of degrees of arc, computed from
    (degrees + minutes/60 + seconds/3600) x direction.

    degrees, minutes and seconds should be strings, ints, floats or None; if all
    are None, None is returned.

    is_latitude should be a bool.

    A ValueError is raised if any of the following is True:
        degrees < 0.0 and direction:
        minutes and not direction:
        seconds and minutes is None:
        is_latitude is True and direction is None or is not in ('N', 'n', 'S', 's')
        is_latitude is False and direction is None or is not in ('E', 'e', 'W', 'w')
        minutes and not 0.0<=minutes<60.0:
        seconds and not 0.0<=seconds<60.0:
        is_latitude is True and for computed value, v, not   -90.0 <= v <=  90.0
        is_latitude is False and for computed value, v, not -180.0 <= v <= 180.0
    """

    direction = direction.lower() if direction else None
    if direction:
        if direction not in ('n', 's', 'e', 'w'):
            msg = u'Unexpected direction [{0}]'
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

    degrees = float(degrees)
    minutes = None if minutes is None else float(minutes)
    seconds = None if seconds is None else float(seconds)

    # Checks
    if degrees < 0.0 and direction:
        raise ValueError(u'Negative degrees with direction')
    elif minutes and not direction:
        raise ValueError(u'Minutes without direction')
    elif seconds and minutes is None:
        raise ValueError(u'Seconds without minutes')
    elif direction and dir_is_latitude != is_latitude:
        raise ValueError(u'Direction mismatch.')
    elif minutes and not float(minutes).is_integer() and seconds:
        msg = u'Both seconds [{0}] and fractional minutes [{1}] given'
        raise ValueError(msg.format(seconds, minutes))
    elif minutes and not 0.0<=minutes<60.0:
        msg = u'Bad minutes [{0}]. Require a number between 0 and 60'
        raise ValueError(msg.format(minutes))
    elif seconds and not 0.0<=seconds<60.0:
        msg = u'Bad seconds [{0}]. Require a number between 0 and 60'
        raise ValueError(msg.format(seconds))
    else:
        # Compute the floating-point degrees of arc
        degrees += minutes / 60.0 if minutes else 0.0
        degrees += seconds / 3600.0 if seconds else 0.0

        degrees *= -1.0 if negate else 1.0

        # Check bounds
        if not is_latitude and not -180 <= degrees <= 180:
            msg = u'Longitude [{0}] is outside of the range -180 to 180'
            raise ValueError(msg.format(degrees))
        elif is_latitude and not -90 <= degrees <= 90:
            msg = u'Computed latitude [{0}] is outside of the range -90 to 90'
            raise ValueError(msg.format(degrees))
        else:
            return degrees

def parse_matches_re(re, error_message, v):
    """Raises ValueError(error_message) if v does not match re
    """
    res = re.match(v)
    if not res:
        raise ValueError(error_message.format(v))
    else:
        return v

def parse_in_choices(choices, v):
    """If v not in choices, raise ValueError(error_message)
    """
    if v not in choices:
        raise ValueError(u'Invalid value [{0}]: not in choices'.format(v))
    else:
        return v
