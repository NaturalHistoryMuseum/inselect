from itertools import count, izip
from pathlib import Path

from PySide.QtGui import QIcon

from inselect.lib.inselect_error import InselectError

from gouda.engines import InliteEngine, LibDMTXEngine
from gouda.strategies import roi, resize

from inselect.lib.utils import debug_print

from .plugin import Plugin


class BarcodePlugin(Plugin):

    def __init__(self, app):
        self.document = None

    @classmethod
    def name(cls):
        """Name of the plugin
        """
        return 'Decode barcodes'

    @classmethod
    def prompt(cls):
        """A description of the effect of running this plugin.
        """
        return ("Will load the full-resolution scanned image and will set each "
                "box's 'Specimen number' metadata field with value(s) of any "
                "barcodes.")

    @classmethod
    def icon(cls):
        dir = Path(__file__).resolve().parents[3]
        return QIcon(str(dir / 'data' / 'barcode_icon.png'))

    def __call__(self, document, progress):
        """
        """
        debug_print('BarcodePlugin.__call__')

        if InliteEngine.available():
            engine = InliteEngine(datamatrix=True)
        elif LibDMTXEngine.available():
            engine = LibDMTXEngine()
        else:
            raise InselectError('No barcode decoding engine available')

        progress(label='Loading full-res image')
        image_array = document.scanned.array

        items = document.items
        for index, item, crop in izip(count(), items, document.crops):
            msg = u'Reading barcodes in box {0} of {1}'.format(1 + index, len(items))
            progress(label=msg)
            barcodes = self._decode_barcodes(engine, crop)
            if barcodes:
                debug_print('Crop [{0}] - found [{1}]'.format(index, barcodes))

                # TODO LH This mapping to come from metadata config?
                # TODO LH Could be more than one specimen, and hence barcode,
                #         on a crop
                item['fields']['Specimen Number'] = barcodes
            else:
                debug_print('Crop [{0}] - no barcodes'.format(index))

        self.items = items

        debug_print('BarcodePlugin.__call__ exiting. [{0}] boxes'.format(len(items)))

    def _decode_barcodes(self, engine, crop):
        for strategy in (resize, roi):
            result = strategy(crop, engine)
            if result:
                strategy, barcodes = result
                return u' '.join([b.data for b in barcodes])
        return None
