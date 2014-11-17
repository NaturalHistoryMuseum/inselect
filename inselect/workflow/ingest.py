#!/usr/bin/env python
"""Ingest scanned images
"""

import argparse
import stat
import traceback

from pathlib import Path

# Import numpy here to prevent PyInstaller build from breaking
# TODO LH find a better solution
import numpy

import inselect
import inselect.lib.utils

from inselect.lib.document import InselectDocument, InselectImage
from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print, make_readonly


def ingest_image(source, dest_dir):
    dest = dest_dir / source.name
    if source!=dest and dest.is_file():
        raise InselectError('Destination image [{0}] exists'.format(dest))
    else:
        debug_print('Ingesting [{0}] to [{1}]'.format(source, dest))
        if source!=dest:
            source.rename(dest)

        # Raises if the document already exists
        doc = InselectDocument.new_from_scan(dest)

        doc.ensure_thumbnail()

        # Make images read-only
        debug_print('Making image files read-only')
        make_readonly(doc.scanned.path)
        make_readonly(doc.thumbnail.path)

        # TODO LH Copy EXIF tags?
        debug_print('Ingested [{0}] to [{1}]'.format(source, dest))

        return doc

def ingest(inbox, docs):
    inbox, docs = Path(inbox), Path(docs)
    if not inbox.is_dir():
        raise InselectError('Inbox directory [{0}] does not exist'.format(inbox))

    if not docs.is_dir():
        print('Create document directory [{0}]'.format(docs))
        docs.mkdir(parents=True)

    for source in inbox.glob('*tiff'):
        try:
            ingest_image(source, docs)
        except Exception:
            print('Error ingesting [{0}]'.format(source))
            traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description='Ingests images into inselect')
    parser.add_argument("inbox", help='Source directory containing scanned images')
    parser.add_argument("docs", help='Destination directory')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + inselect.__version__)
    args = parser.parse_args()

    inselect.lib.utils.DEBUG_PRINT = args.verbose

    ingest(args.inbox, args.docs)

if __name__=='__main__':
    main()
