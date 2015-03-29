#!/usr/bin/env python
"""Saves cropped object images
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
from inselect.lib.document_export import DocumentExport
from inselect.lib.metadata_library import library
from inselect.lib.utils import debug_print


# TODO Recursive option
# TODO Ignore documents that fail validation; option to ignore failures

def save_crops(dir, overwrite_existing, metadata_template):
    dir = Path(dir)
    export = DocumentExport(metadata_template)
    for p in dir.glob('*' + InselectDocument.EXTENSION):
        try:
            debug_print('Loading [{0}]'.format(p))
            doc = InselectDocument.load(p)
            if not overwrite_existing and doc.crops_dir.is_dir():
                print('Crops dir [{0}] exists - skipping'.format(doc.crops_dir))
            else:
                print('Will save crops for [{0}] to [{1}]'.format(p, doc.crops_dir))

                debug_print('Loading full-resolution scanned image')
                doc.scanned.array

                debug_print('Saving crops')
                export.save_crops(doc)
        except Exception:
            print('Error saving crops from [{0}]'.format(p))
            traceback.print_exc()


def main():
    parser = argparse.ArgumentParser(
        description='Writes cropped object images from Inselect documents')
    parser.add_argument("dir", help='Directory containing Inselect documents')
    parser.add_argument('-o', '--overwrite', action='store_true',
        help='Overwrite existing crops directories')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('--template',
        help=('Use a metadata template to validate documents and generate '
              'filenames of xcrops'), choices=library().keys())
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + inselect.__version__)
    args = parser.parse_args()

    inselect.lib.utils.DEBUG_PRINT = args.debug

    save_crops(args.dir, args.overwrite, library().get(args.template))


if __name__=='__main__':
    main()
