from itertools import count, izip
from pathlib import Path

from PySide.QtGui import QIcon

from inselect.gui import icons
from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print

from .plugin import Plugin

try:
    import gouda
    from gouda.engines import InliteEngine, LibDMTXEngine
    from gouda.strategies import roi, resize
except ImportError:
    gouda = None


class BarcodePlugin(Plugin):

    def __init__(self, document, parent):
        if not gouda:
            raise InselectError('Barcode decoding is not available')
        else:
            self.document = document

    @classmethod
    def name(cls):
        """Name of the plugin
        """
        return 'Decode barcodes'

    @classmethod
    def description(cls):
        """A description of the effect of running this plugin.
        """
        return ("Will load the full-resolution scanned image and will set each "
                "box's 'Specimen number' metadata field with value(s) of any "
                "barcodes.")

    @classmethod
    def icon(cls):
        return QIcon(":/data/barcode_icon.png")

    def __call__(self, progress):
        """
        """
        debug_print('BarcodePlugin.__call__')

        if InliteEngine.available():
            engine = InliteEngine(datamatrix=True)
        elif LibDMTXEngine.available():
            engine = LibDMTXEngine()
        else:
            raise InselectError('No barcode decoding engine available')

        progress('Loading full-res image')
        image_array = self.document.scanned.array

        items = self.document.items
        for index, item, crop in izip(count(), items, self.document.crops):
            msg = u'Reading barcodes in box {0} of {1}'.format(1 + index, len(items))
            progress(msg)
            barcodes = self._decode_barcodes(engine, crop, progress)
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

    def _decode_barcodes(self, engine, crop, progress):
        for strategy in (resize, roi):
            # TODO LH Must be able to cancel within call to strategy
            progress()
            result = strategy(crop, engine)
            if result:
                strategy, barcodes = result
                return u' '.join([b.data for b in barcodes])
        return None
