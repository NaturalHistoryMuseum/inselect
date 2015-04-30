#!/usr/bin/env python
"""Ingests scanned images
"""

import argparse
import re
import stat
import traceback

from itertools import chain
from pathlib import Path

# Import numpy here to prevent PyInstaller build from breaking
# TODO LH find a better solution
import numpy

import inselect
import inselect.lib.utils

from inselect.lib.ingest import ingest_image, IMAGE_PATTERNS

from inselect.lib.inselect_error import InselectError


# TODO Recursive option

def ingest_from_directory(inbox, docs):
    """Ingest images from the directory given by inbox to the directory given
    by docs
    """
    inbox, docs = Path(inbox), Path(docs)
    if not inbox.is_dir():
        raise InselectError('Inbox directory [{0}] does not exist'.format(inbox))

    if not docs.is_dir():
        print(('Create document directory [{0}]'.format(docs)))
        docs.mkdir(parents=True)

    # TODO LH Case insensitive matching
    for source in chain(*[inbox.glob(p) for p in IMAGE_PATTERNS]):
        print(('Ingesting [{0}]'.format(source)))
        try:
            ingest_image(source, docs)
        except Exception:
            print(('Error ingesting [{0}]'.format(source)))
            traceback.print_exc()
        else:
            print(('Ingested [{0}]'.format(source)))


def main():
    parser = argparse.ArgumentParser(description='Ingests images into Inselect')
    parser.add_argument("inbox", help='Source directory containing scanned images')
    parser.add_argument("docs", help='Destination directory to which images '
                        'will be moved and in which Inselect documents will be '
                        'created. Can be the same as inbox.')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + inselect.__version__)
    args = parser.parse_args()

    inselect.lib.utils.DEBUG_PRINT = args.debug

    ingest_from_directory(args.inbox, args.docs)


if __name__=='__main__':
    main()
