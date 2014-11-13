"""Segment documents
"""
import argparse
import traceback

from pathlib import Path

# Import numpy here to prevent PyInstaller build from breaking
# TODO LH find a better solution
import numpy

import inselect.lib.utils

from inselect.lib.document import InselectDocument
from inselect.lib.segment import segment_edges
from inselect.lib.utils import debug_print
from inselect.lib.rect import Rect


def segment(dir):
    dir = Path(dir)
    for p in dir.glob('*' + InselectDocument.EXTENSION):
        doc = InselectDocument.load(p)
        if not doc.items:
            try:
                debug_print('Will segment [{0}]'.format(p))

                # TODO LH This logic belongs in a Segmenter class
                if doc.thumbnail:
                    debug_print('Will segment on thumbnail')
                    img = doc.thumbnail
                else:
                    debug_print('Will segment on scan')
                    img = doc.scanned

                debug_print('Segmenting [{0}]'.format(p))
                rects,junk = segment_edges(img.array,
                                           variance_threshold=100,
                                           size_filter=1)
                rects = map(lambda r: Rect(r[0], r[1], r[2], r[3]), rects)
                rects = img.to_normalised(rects)
                items = [{"fields": {}, 'rect': r} for r in rects]
                doc.set_items(items)
                doc.save()
            except Exception:
                print('Error segmenting [{0}]'.format(p))
                traceback.print_exc()
        else:
            print('Skipping [{0}] as it already contains items'.format(p))

def main():
    parser = argparse.ArgumentParser(description='Segments inselect documents')
    parser.add_argument("dir", help='Directory containing inselect documents')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + inselect.__version__)
    args = parser.parse_args()

    inselect.lib.utils.DEBUG_PRINT = args.verbose

    segment(args.dir)

if __name__=='__main__':
    main()
