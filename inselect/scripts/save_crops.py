#!/usr/bin/env python
"""Saves cropped object images
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

from inselect.lib.document import InselectDocument
from inselect.lib.document_export import DocumentExport
from inselect.lib.templates.dwc import DWC
from inselect.lib.utils import debug_print
from inselect.lib.user_template import UserTemplate
from inselect.lib.validate_document import format_validation_problems


# TODO Recursive option

def save_crops(dir, overwrite_existing, template):
    dir = Path(dir)
    export = DocumentExport(UserTemplate.load(template) if template else DWC)
    for p in dir.glob('*' + InselectDocument.EXTENSION):
        try:
            debug_print('Loading [{0}]'.format(p))
            doc = InselectDocument.load(p)
            validation = export.validation_problems(doc)
            if validation.any_problems:
                print(
                    u'Not saving crops for [{0}] because there are validation '
                    u'problems'.format(p)
                )
                for msg in format_validation_problems(validation):
                    print(msg)
            elif not overwrite_existing and doc.crops_dir.is_dir():
                print(u'Crops dir [{0}] exists - skipping'.format(doc.crops_dir))
            else:
                print(u'Will save crops for [{0}] to [{1}]'.format(p, doc.crops_dir))

                debug_print(u'Loading full-resolution scanned image')
                doc.scanned.array

                debug_print(u'Saving crops')
                export.save_crops(doc)
        except KeyboardInterrupt:
            raise
        except Exception:
            print(u'Error saving crops from [{0}]'.format(p))
            traceback.print_exc()


def main(args):
    parser = argparse.ArgumentParser(
        description='Writes cropped object images from Inselect documents'
    )
    parser.add_argument("dir", type=Path,
                        help='Directory containing Inselect documents')
    parser.add_argument('-o', '--overwrite', action='store_true',
                        help='Overwrite existing crops directories')
    parser.add_argument(
        '-t', '--template', type=Path, help="Path to a '{0}' file that will be "
        'used to format the crop filenames'.format(UserTemplate.EXTENSION)
    )
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + inselect.__version__)
    args = parser.parse_args(args)

    inselect.lib.utils.DEBUG_PRINT = args.debug

    save_crops(args.dir, args.overwrite, args.template)


if __name__ == '__main__':
    main(sys.argv[1:])
