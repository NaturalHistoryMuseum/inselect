"""Post-process
"""
import argparse
import operator

from itertools import izip
from pathlib import Path


import inselect.lib.utils

from inselect.lib import config
from inselect.lib.utils import debug_print
from inselect.lib.document import InselectDocument


from gouda.bin.decode_barcode import decode_barcodes
from gouda.decode import ZbarDecoder, SoftekDecoder


def post_process(dir):
    dir = Path(dir)

    # TODO LH Workers from metadata config?
    workers = [ZbarDecoder(),
               SoftekDecoder(),
              ]

    for p in dir.glob('*' + InselectDocument.EXTENSION):
        # TODO LH Do not do this for documents that have been post-processed
        metadata_from_barcodes(InselectDocument.load(p), workers)

def metadata_from_barcodes(doc, workers):
    items = doc.items
    for item, crop in izip(items, doc.crops):
        barcodes = decode_barcodes(crop, workers)
        if barcodes:
            barcodes = u' '.join(barcodes)
            debug_print('Found barcodes [{0}]'.format(barcodes))
            # TODO LH This mapping from metadata config?
            item['fields']['Specimen Number'] = barcodes

    doc.set_items(items)
    doc.save()

def main():
    parser = argparse.ArgumentParser(description='Post-processes pending documents')
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('-v', '--version', action='version', 
                        version='%(prog)s ' + inselect.__version__)
    args = parser.parse_args()

    inselect.lib.utils.DEBUG_PRINT = args.verbose

    post_process(config.inselect)

if __name__=='__main__':
    main()
