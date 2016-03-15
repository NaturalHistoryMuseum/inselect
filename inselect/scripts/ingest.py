#!/usr/bin/env python
"""Ingests scanned images
"""
from __future__ import print_function

import argparse
import sys
import traceback

from pathlib import Path

# Import numpy here to prevent PyInstaller build from breaking
# TODO LH find a better solution
import numpy    # noqa

import inselect
import inselect.lib.utils

from inselect.lib.cookie_cutter import CookieCutter
from inselect.lib.ingest import ingest_image, IMAGE_SUFFIXES_RE

from inselect.lib.inselect_error import InselectError


# TODO Recursive option

def ingest_from_directory(inbox, docs, cookie_cutter=None):
    """Ingest images from the directory given by inbox to the directory given
    by docs
    """
    inbox, docs = Path(inbox), Path(docs)
    cookie_cutter = Path(cookie_cutter) if cookie_cutter else None
    if not inbox.is_dir():
        raise InselectError(u'Inbox directory [{0}] does not exist'.format(inbox))

    if not docs.is_dir():
        print(u'Create document directory [{0}]'.format(docs))
        docs.mkdir(parents=True)

    if cookie_cutter:
        cookie_cutter = CookieCutter.load(cookie_cutter)

    for source in (p for p in inbox.iterdir() if IMAGE_SUFFIXES_RE.match(p.name)):
        print(u'Ingesting [{0}]'.format(source))
        try:
            ingest_image(source, docs, cookie_cutter=cookie_cutter)
        except Exception:
            print(u'Error ingesting [{0}]'.format(source))
            traceback.print_exc()
        else:
            print(u'Ingested [{0}]'.format(source))


def main(args):
    parser = argparse.ArgumentParser(description='Ingests images into Inselect')
    parser.add_argument("inbox", help='Source directory containing scanned images')
    parser.add_argument("docs", help='Destination directory to which images '
        'will be moved and in which Inselect documents will be created. Can be '
        'the same as inbox.')
    parser.add_argument('-c', '--cookie-cutter', help="Path to a '{0}' file "
        'that will be applied to new Inselect '
        'documents'.format(CookieCutter.EXTENSION)
    )
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + inselect.__version__)
    args = parser.parse_args(args)

    inselect.lib.utils.DEBUG_PRINT = args.debug

    ingest_from_directory(args.inbox, args.docs, args.cookie_cutter)


if __name__ == '__main__':
    main(sys.argv[1:])
