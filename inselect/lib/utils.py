from __future__ import print_function

import errno
import locale
import os
import shutil
import stat
import string

from collections import Counter
from itertools import ifilterfalse
from pathlib import Path

from dateutil.tz import tzlocal

try:
    import pwd
except ImportError:
    pwd = None

try:
    import win32api
except ImportError:
    win32api = None


DEBUG_PRINT = False
DEFAULT_LOCALE = None


def debug_print(*args, **kwargs):
    if DEBUG_PRINT:
        print(*args, **kwargs)


def get_default_locale():
    """Returns cached result of locale.getdefaultlocale()
    """
    global DEFAULT_LOCALE
    if not DEFAULT_LOCALE:
        DEFAULT_LOCALE = locale.getdefaultlocale()
        debug_print('Loaded default locale [{0}]'.format(DEFAULT_LOCALE))
    return DEFAULT_LOCALE


def is_writable(path):
    """Returns True is path is writable
    """
    return bool(Path(path).stat()[stat.ST_MODE] & stat.S_IWUSR)


def make_readonly(path):
    """Alters path to be read-only and return the original mode
    """
    path = Path(path)
    mode = path.stat()[stat.ST_MODE]
    path.chmod(mode ^ (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
    return mode


def rmtree_readonly(path):
    """Like shutil.rmtree() but removes read-only files on Windows
    """

    # http://stackoverflow.com/a/9735134
    def handle_remove_readonly(func, path, exc):
        excvalue = exc[1]
        if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:

            # ensure parent directory is writeable too
            pardir = os.path.abspath(os.path.join(path, os.path.pardir))
            if not os.access(pardir, os.W_OK):
                os.chmod(pardir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)

            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777

            func(path)
        else:
            raise

    shutil.rmtree(str(path), ignore_errors=False, onerror=handle_remove_readonly)


def unique_everseen(iterable, key=None):
    "List unique elements, preserving order. Remember all elements ever seen."
    # Taken from https://docs.python.org/2/library/itertools.html
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in ifilterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


def duplicated(v):
    """Returns a generator expression of values within v that appear more than
    once
    """
    return (x for x, y in Counter(v).items() if y > 1)


class FormatDefault(string.Formatter):
    """A string formatter than returns a default value for missing keys
    http://stackoverflow.com/a/19800610

    >>> fmt = FormatDefault(default='???')
    >>> metadata = {'catalogNumber' : '1234'}
    >>> template = '{catalogNumber}-{x}'
    >>> print(fmt.format(template, **metadata))
    '1234-???'

    """
    def __init__(self, default=''):
        self.default = default

    def get_value(self, key, args, kwds):
        # key will be either an integer or a string. If it is an integer, it
        # represents the index of the positional argument in args; if it is
        # a string, then it represents a named argument in kwargs.
        if isinstance(key, (int, long)):
            return super(FormatDefault, self).get_value(key, args, kwds)
        else:
            return kwds.get(key, self.default)


def user_name():
    """The name of the current user
    """
    if pwd:
        # Strip trailing commas seen on Linux
        return pwd.getpwuid(os.getuid()).pw_gecos.rstrip(',')
    else:
        try:
            import pywintypes
            import win32api
        except ImportError:
            pass
        else:
            NameDisplay = 3
            try:
                # Returns Unicode
                return win32api.GetUserNameEx(NameDisplay)
            except pywintypes.error:
                try:
                    # Returns MBCS
                    return unicode(win32api.GetUserName(), 'mbcs')
                except pywintypes.error:
                    return ''

    return ''


def format_dt_display(dt):
    """Returns a local-time string representation of the datetime instance dt
    """
    # Convert tz-aware datetime to local time zone
    if dt.tzinfo:
        dt = dt.astimezone(tzlocal())

    if hasattr(locale, 'nl_langinfo'):
        # nl_langinfo "...is not available on all systems, and the set of
        # possible options might also vary across platforms"
        v = dt.strftime(locale.nl_langinfo(locale.D_T_FMT))
        # strftime "...output may contain Unicode characters encoded using the
        # locale's default encoding"
        # locale.getlocale() is not the correct function to use - use
        # locale.getdefaultlocale()
        # encoding might be None
        language_code, encoding = get_default_locale()
        # Ignoring errors because I am paranoid about the behaviour of the
        # locale functions
        if encoding:
            return unicode(v, encoding, 'ignore')
        else:
            return unicode(v, errors='ignore')
    elif win32api:
        # https://msdn.microsoft.com/en-us/library/dd373901(v=vs.85).aspx
        LOCALE_USER_DEFAULT = 0x0400
        DATE_LONGDATE = 2
        time = win32api.GetTimeFormat(LOCALE_USER_DEFAULT, 0, dt)
        time = unicode(time, "mbcs")
        date = win32api.GetDateFormat(LOCALE_USER_DEFAULT, DATE_LONGDATE, dt)
        date = unicode(date, "mbcs")
        return u'{0} {1}'.format(date, time)

    return dt.isoformat()
