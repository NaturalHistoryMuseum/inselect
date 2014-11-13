"""Post-process
"""
import argparse
import operator

from itertools import izip
from pathlib import Path

# Import numpy here to prevent PyInstaller build from breaking
# TODO LH find a better solution
import numpy

import inselect.lib.utils

from inselect.lib.utils import debug_print
from inselect.lib.document import InselectDocument
from inselect.lib.inselect_error import InselectError

from gouda.strategies import roi, resize
from gouda.engines import (AccusoftEngine, DataSymbolEngine,
                           InliteEngine, LibDMTXEngine, StecosEngine,
                           SoftekEngine, ZbarEngine, ZxingEngine)


def create_datamatrix_engine():
    # Preferred Data Matrix decoders
    if InliteEngine.available():
        return InliteEngine(datamatrix=True)
    elif AccusoftEngine.available():
        return AccusoftEngine(datamatrix=True)
    elif SoftekEngine.available():
        return SoftekEngine(datamatrix=True)
    elif LibDMTXEngine.available():
        return LibDMTXEngine()
    else:
        raise InselectError('No engine for Data Matrix')

def read_barcodes(dir):
    # TODO LH Engines from metadata config
    engine = create_datamatrix_engine()
    for p in dir.glob('*' + InselectDocument.EXTENSION):
        # TODO LH Do not overwrite existing specimen numbers or whatever field
        # it is that barcodes are written to
        print(p)
        try:
            read_barcodes_in_document(InselectDocument.load(p), engines)
        except Exception:
            print('Error reading barcodes in [{0}]'.format(p))
            traceback.print_exc()

def decode_barcodes(crop, engines):
    for strategy in (resize, roi):
        barcodes = strategy(img, engines)
        if barcodes:
            return barcodes
    return []

def read_barcodes_in_document(doc, engines):
    items = doc.items
    for item, crop in izip(items, doc.crops):
        barcodes = decode_barcodes(crop, engines)
        if barcodes:
            barcodes = u' '.join([b.data for b in barcodes])
            debug_print('Found barcodes [{0}]'.format(barcodes))
            # TODO LH This mapping from metadata config?
            item['fields']['Specimen Number'] = barcodes

    doc.set_items(items)
    doc.save()

def main():
    parser = argparse.ArgumentParser(description='Read barcodes in cropped specimens')
    parser.add_argument("dir", help='Directory containing inselect documents')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--debug-barcodes', action='store_true')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + inselect.__version__)
    args = parser.parse_args()

    inselect.lib.utils.DEBUG_PRINT = args.verbose
    gouda.util.DEBUG_PRINT = args.debug_barcodes

    read_barcodes(Path(args.dir))

if __name__=='__main__':
    main()
