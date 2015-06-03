import calendar
import datetime

from .inselect_error import InselectError


class SparseDate(object):
    """ A date where each component is optional. """

    _LEVELS = {'year' : 0,
               'month': 1,
               'day':   2,
             }

    def __init__(self, year, month, day):
        """Each component is optional.

        A ValueError is raised if month is provided and year is not.
        A ValueError is raised if day is provded and month is not.
        """

        if not year:
            raise ValueError('Year missing')
        else:
            if day is not None and month is None:
                raise ValueError('Day was given but year was not')

            if not isinstance(year, int):
                raise ValueError('Year should be an integer')
            elif month is not None:
                if not isinstance(month, int):
                    raise ValueError('Month should be an integer')

                # Check month and day ranges
                if not 0<month<13:
                    msg = 'Bad month [{0}]: require a number between 1 and 12'
                    raise ValueError(msg.format(month))

                if day is not None:
                    if not isinstance(day, int):
                        raise ValueError('Day should be an integer')

                    days_in_month = calendar.monthrange(year, month)[1]
                    if day is not None and not 0<day<=days_in_month:
                        msg = 'Bad day [{0}]: require a number between 1 and {1}'
                        raise ValueError(msg.format(day, days_in_month))

            self._year = year
            self._month = month if month else None
            self._day = day if day else None

    @property
    def resolution(self):
        "'year', 'month' or 'day'"
        if self._day:
            return 'day'
        elif self._month:
            return 'month'
        else:
            return 'year'

    def __repr__(self):
        return 'SparseDate({0}, {1}, {2})'.format(self._year, self._month, self._day)

    def __str__(self):
        return '{0}-{1}-{2}'.format(self._year, self._month, self._day)

    def __iter__(self):
        return iter( (self._year, self._month, self._day) )

    def as_date(self):
        """Returns a datetime.date, if resolution is 'day'. Raises a
        InselectError otherwise
        """
        if self._day:
            return datetime.date(self._year, self._month, self._day)
        else:
            raise InselectError('Insufficient resolution')

    def earliest(self):
        """Returns a SparseDate of the earliest of the range represented by
        self"""
        if self._day:
            return self
        else:
            return SparseDate(self._year,
                              self._month if self._month else 1,
                              self._day if self._day else 1)

    def latest(self):
        """Returns a SparseDate of the latest of the range represented by
        self"""
        if self._day:
            return self
        else:
            year = self._year
            month = self._month if self._month else 12
            day = self.day if self._day else calendar.monthrange(year, month)[1]
            return SparseDate(year, month, day)

    @classmethod
    def downsample_to_common(cls, dates):
        "Returns the list of dates downsampled to the lowest resolution"
        to = min([d._LEVELS[d.resolution] for d in dates])
        return [d._downsample_to_level(to) for d in dates]

    def downsample(self, to):
        """Returns self downsampled. 'to' should be one of 'year', 'month',
        'day' or None
        """
        if to not in self._LEVELS:
            raise ValueError('Not a valid resolution [{0}]'.format(to))
        else:
            return self._downsample_to_level(self._LEVELS[to])

    def _downsample_to_level(self, to):
        " Returns self downsampled. 'to' should a value of self._LEVELS "
        current = self._LEVELS[self.resolution]
        if to>current:
            msg = 'Cannot increase resolution from [{0}] to [{1}]'
            raise ValueError(msg.format(current, to))
        elif 0==to:
            return SparseDate(self._year, None, None)
        elif 1==to:
            return SparseDate(self._year, self._month, None)
        elif 2==to:
            return SparseDate(self._year, self._month, self._day)

    def _pre_compare(self, other):
        "Raises an exception if self and other cannot be compared"
        if not isinstance(other, SparseDate):
            raise NotImplementedError()
        elif self.resolution != other.resolution:
            msg = 'Cannot compare SparseDates of different resolutions'
            raise InselectError(msg)

    def __eq__(self, other):
        self._pre_compare(other)
        return tuple(self) == tuple(other)

    def __ne__(self, other):
        self._pre_compare(other)
        return tuple(self) != tuple(other)

    def __le__(self, other):
        self._pre_compare(other)
        return tuple(self) <= tuple(other)

    def __lt__(self, other):
        self._pre_compare(other)
        return tuple(self) < tuple(other)

    def __ge__(self, other):
        self._pre_compare(other)
        return tuple(self) >= tuple(other)

    def __gt__(self, other):
        self._pre_compare(other)
        return tuple(self) > tuple(other)

    def __hash__(self):
        return hash(tuple(self))
