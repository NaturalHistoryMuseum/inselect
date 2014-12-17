from __future__ import print_function

import stat

from pathlib import Path

from inselect.lib.inselect_error import InselectError

DEBUG_PRINT = False


def debug_print(*args, **kwargs):
    if DEBUG_PRINT:
        print(*args, **kwargs)

def make_readonly(path):
    path = Path(path)
    mode = path.stat()[stat.ST_MODE]
    path.chmod(mode ^ (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))

def validate_normalised(boxes):
    for l,t,w,h in boxes:
        if not (l>=0 and t>=0 and l<=1 and t<=1 and w>0 and l+w<=1 and h>0 and
                t+h<=1):
            raise InselectError('One or more boxes are not normalised')

