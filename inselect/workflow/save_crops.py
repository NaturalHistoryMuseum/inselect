#!/usr/bin/env python
"""Save cropped speciment images
"""

import argparse
import traceback

from pathlib import Path

# Import numpy here to prevent PyInstaller build from breaking
# TODO LH find a better solution
import numpy

import inselect
import inselect.lib.utils

from inselect.lib.document import InselectDocument
from inselect.lib.utils import debug_print


# TODO Ignore if existing crops dir; option to overwrite

def save_crops(dir):
    dir = Path(dir)
    for p in dir.glob('*' + InselectDocument.EXTENSION):
        try:
            debug_print('Will save crops from [{0}]'.format(p))
            doc = InselectDocument.load(p)

            debug_print('Loading full-resolution scanned image')
            doc.scanned.array

            debug_print('Saving crops')
            doc.save_crops()
        except Exception:
            print('Error save crops from [{0}]'.format(p))
            traceback.print_exc()


def main():
    parser = argparse.ArgumentParser(description='Writes cropped specimen images')
    parser.add_argument("dir", help='Directory containing inselect documents')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + inselect.__version__)
    args = parser.parse_args()

    inselect.lib.utils.DEBUG_PRINT = args.debug

    save_crops(args.dir)

if __name__=='__main__':
    main()
