#!/usr/bin/env python
"""Exports metadata
"""
from __future__ import print_function

import argparse
import traceback

from pathlib import Path

# Import numpy here to prevent PyInstaller build from breaking
# TODO LH find a better solution
import numpy    # noqa

import inselect
import inselect.lib.utils

from inselect.lib.document import InselectDocument
from inselect.lib.document_export import DocumentExport
from inselect.lib.templates.dwc import DWC
from inselect.lib.utils import debug_print


# TODO Recursive option
# TODO Ignore existing CSV files; option to overwrite

def export_csv(dir, overwrite_existing):
    dir = Path(dir)
    # TODO Template name as argument
    export = DocumentExport(DWC)
    for p in dir.glob('*' + InselectDocument.EXTENSION):
        try:
            debug_print('Loading [{0}]'.format(p))
            doc = InselectDocument.load(p)
            csv_path = export.csv_path(doc)
            if not overwrite_existing and csv_path.is_file():
                print('CSV file [{0}] exists - skipping'.format(csv_path))
            else:
                print('Will write CSV for [{0}]'.format(p))
                export.export_csv(doc)
        except Exception:
            print('Error saving CSV from [{0}]'.format(p))
            traceback.print_exc()


def main():
    parser = argparse.ArgumentParser(description='Exports metadata from Inselect documents')
    parser.add_argument("dir", help='Directory containing Inselect documents')
    parser.add_argument('-o', '--overwrite', action='store_true',
                        help='Overwrite existing metadata files')
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + inselect.__version__)
    args = parser.parse_args()

    inselect.lib.utils.DEBUG_PRINT = args.debug

    export_csv(args.dir, args.overwrite)

if __name__ == '__main__':
    main()
