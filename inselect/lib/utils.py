from __future__ import print_function

import errno
import os
import stat
import shutil

from collections import Counter
from itertools import ifilterfalse
from pathlib import Path

from inselect.lib.inselect_error import InselectError

DEBUG_PRINT = False


def debug_print(*args, **kwargs):
    if DEBUG_PRINT:
        print(*args, **kwargs)

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
                os.chmod(pardir, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO)

            os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO) # 0777

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
    """Returns values within v that appear more than once
    """
    return [x for x, y in Counter(v).items() if y > 1]
