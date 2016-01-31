#!/usr/bin/env python
"""Segment documents
"""
import argparse
import traceback

from pathlib import Path

# Import numpy here to prevent PyInstaller build from breaking
# TODO LH find a better solution
import numpy    # noqa

import inselect.lib.utils

from inselect.lib.document import InselectDocument
from inselect.lib.segment import segment_document
from inselect.lib.utils import debug_print


# TODO Recursive option
# TODO Option to resegment documents with existing boxes

def segment(dir):
    dir = Path(dir)
    for p in dir.glob('*' + InselectDocument.EXTENSION):
        doc = InselectDocument.load(p)
        if not doc.items:
            print('Segmenting [{0}]'.format(p))
            try:
                debug_print('Will segment [{0}]'.format(p))
                doc, display_image = segment_document(doc)
                del display_image    # We don't use this
                doc.save()
            except Exception:
                print('Error segmenting [{0}]'.format(p))
                traceback.print_exc()
            else:
                print('Segmented [{0}]'.format(doc))
        else:
            print('Skipping [{0}] as it already contains items'.format(p))


def main():
    parser = argparse.ArgumentParser(description='Segments Inselect documents')
    parser.add_argument("dir", help='Directory containing Inselect documents')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + inselect.__version__)
    args = parser.parse_args()

    inselect.lib.utils.DEBUG_PRINT = args.debug

    segment(args.dir)

if __name__ == '__main__':
    main()
