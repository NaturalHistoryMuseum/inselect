#!/usr/bin/env python3
"""Read barcodes in existing documents
"""
from inselect.lib.fix_frozen import fix_frozen

fix_frozen()

import argparse
import sys
import traceback

from itertools import count
from pathlib import Path

import inselect.lib.utils

from inselect.lib.document import InselectDocument
from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print

# Warning: lazy load of gouda via local imports

class BarcodeReader(object):
    def __init__(self, engine, strategies):
        self.engine = engine
        self.strategies = strategies

    def process_dir(self, dir):
        # TODO LH Read image from crops dir, if it exists?
        for p in Path(dir).glob('*' + InselectDocument.EXTENSION):
            # TODO LH Do not overwrite existing object numbers, or whatever
            # field it is that barcodes are written to
            print(p)
            try:
                self.read_barcodes_in_document(InselectDocument.load(p))
            except KeyboardInterrupt:
                raise
            except Exception:
                print('Error reading barcodes in [{0}]'.format(p))
                traceback.print_exc()

    def read_barcodes_in_document(self, doc):
        items = doc.items
        for index, item, crop in zip(count(), items, doc.crops):
            result = self.decode_barcodes(crop)
            if result:
                strategy, barcodes = result
                # data could be either str or bytes
                barcodes = (
                    b.data.decode() if hasattr(b.data, 'decode') else b.data
                    for b in barcodes
                )
                barcodes = ' '.join(sorted(barcodes))
                debug_print('Crop [{0}] - found [{1}]'.format(index, barcodes))

                # TODO LH This mapping to come from metadata config?
                # TODO LH Could be more than one object, and hence barcode,
                #         on a crop
                item['fields']['catalogNumber'] = barcodes
            else:
                debug_print('Crop [{0}] - no barcodes'.format(index))

        doc.set_items(items)
        doc.save()

    def decode_barcodes(self, crop):
        for strategy in self.strategies:
            result = strategy(crop, self.engine)
            if result:
                return result
        return None


def read_barcodes(engine, dir, strategies):
    BarcodeReader(engine, strategies).process_dir(dir)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    # Private import to avoid top-level import of cv2 (via gouda), which
    # would make the script slower to start and potentially break if
    # frozen on Windows (see call to fix_frozen_dll_path below).
    try:
        import gouda
    except ImportError:
        gouda = engine_options = None
    else:
        from gouda.engines.options import engine_options
        from gouda.strategies.resize import resize
        from gouda.strategies.roi.roi import roi

    if not gouda:
        raise InselectError('Barcode decoding not available')
    options = engine_options()
    if not options:
        raise InselectError('No barcode reading engines are available')

    parser = argparse.ArgumentParser(
        description='Reads barcodes within boxes, overwriting existing values'
    )
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--debug-barcodes', action='store_true')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + inselect.__version__)
    parser.add_argument("dir", type=Path,
                        help='Directory containing inselect documents')
    parser.add_argument('engine', choices=sorted(options.keys()),
                        help='The barcode reading engine to use')
    args = parser.parse_args(args)

    inselect.lib.utils.DEBUG_PRINT = args.debug
    gouda.util.DEBUG_PRINT = args.debug_barcodes
    engine = options[args.engine]()
    read_barcodes(engine, args.dir, strategies=(resize, roi))


if __name__ in ('__main__', 'read_barcodes__main__'):
    main()
