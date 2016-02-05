#!/usr/bin/env python
"""Post-process
"""
from __future__ import print_function

import argparse
import traceback

from functools import partial
from itertools import count, izip
from pathlib import Path

# Import numpy here to prevent PyInstaller build from breaking
# TODO LH find a better solution
import numpy    # noqa

import inselect.lib.utils

from inselect.lib.utils import debug_print
from inselect.lib.document import InselectDocument
from inselect.lib.inselect_error import InselectError

try:
    import gouda

    from gouda.engines import (AccusoftEngine, InliteEngine, LibDMTXEngine,
                               SoftekEngine)
    from gouda.strategies.resize import resize
    from gouda.strategies.roi.roi import roi
except ImportError:
    gouda = None

# TODO LH Engine from metadata config


def _datamatrix_engine():
    """Returns callable that is the preferred database engine
    """
    engines = [
        (InliteEngine, partial(InliteEngine, datamatrix=True)),
        (AccusoftEngine, partial(AccusoftEngine, datamatrix=True)),
        (SoftekEngine, partial(SoftekEngine, datamatrix=True)),
        (LibDMTXEngine, LibDMTXEngine),
    ]
    engines = [f for e, f in engines if e.available()]
    return engines[0] if engines else None

DATAMATRIX_ENGINE = _datamatrix_engine()


class BarcodeReader(object):
    def __init__(self, debug_barcodes):
        if not gouda:
            raise InselectError('Barcode decoding not available')
        elif not DATAMATRIX_ENGINE:
            raise InselectError('No datamatrix engine available')
        else:
            self.engine = DATAMATRIX_ENGINE()
            gouda.util.DEBUG_PRINT = debug_barcodes

    @classmethod
    def available(cls):
        return gouda is not None and DATAMATRIX_ENGINE is not None

    def process_dir(self, dir):
        # TODO LH Read image from crops dir, if it exists?
        for p in dir.glob('*' + InselectDocument.EXTENSION):
            # TODO LH Do not overwrite existing object numbers, or whatever
            # field it is that barcodes are written to
            print(p)
            try:
                self.read_barcodes_in_document(InselectDocument.load(p))
            except Exception:
                print('Error reading barcodes in [{0}]'.format(p))
                traceback.print_exc()

    def read_barcodes_in_document(self, doc):
        items = doc.items
        for index, item, crop in izip(count(), items, doc.crops):
            result = self.decode_barcodes(crop)
            if result:
                strategy, barcodes = result
                barcodes = u' '.join([b.data for b in barcodes])
                debug_print('Crop [{0}] - found [{1}]'.format(index, barcodes))

                # TODO LH This mapping to come from metadata config?
                # TODO LH Could be more than one object, and hence barcode,
                #         on a crop
                item['fields']['Specimen Number'] = barcodes
            else:
                debug_print('Crop [{0}] - no barcodes'.format(index))

        doc.set_items(items)
        doc.save()

    def decode_barcodes(self, crop):
        for strategy in (resize, roi):
            result = strategy(crop, self.engine)
            if result:
                return result
        return None


def main():
    parser = argparse.ArgumentParser(description='Reads barcodes within boxes')
    parser.add_argument("dir", help='Directory containing inselect documents')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--debug-barcodes', action='store_true')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + inselect.__version__)
    args = parser.parse_args()

    inselect.lib.utils.DEBUG_PRINT = args.debug
    # BarcodeReader will raise error is barcode decoding is not available
    BarcodeReader(args.debug_barcodes).process_dir(Path(args.dir))


if __name__ == '__main__':
    main()
