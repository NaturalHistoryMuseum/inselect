from __future__ import print_function

import stat

from pathlib import Path

DEBUG_PRINT = False


def debug_print(*args, **kwargs):
    if DEBUG_PRINT:
        print(*args, **kwargs)

def make_readonly(path):
    path = Path(path)
    mode = path.stat()[stat.ST_MODE]
    path.chmod(mode ^ (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
