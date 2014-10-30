from __future__ import print_function

import os
import stat

from pathlib import Path

DEBUG_PRINT = False


def debug_print(*args, **kwargs):
    if DEBUG_PRINT:
        print(*args, **kwargs)

def get_corners(x1, y1, x2, y2):
    """Given two diagonally opposite corners of a box, return the top left and
    bottom right corners

    Parameters
    ----------
    x1 : float
    y1 : float
    x2 : float
    y2 : float

    Returns
    -------
    tuple
    """
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    return (x1, y1), (x2, y2)

def make_readonly(path):
    path = Path(path)
    mode = path.stat()[stat.ST_MODE]
    path.chmod(mode ^ (stat.S_IWUSR & stat.S_IWGRP & stat.S_IWOTH))
