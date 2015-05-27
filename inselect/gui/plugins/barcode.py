from itertools import count, izip

from PySide.QtCore import QSettings
from PySide.QtGui import QIcon

from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print

from .plugin import Plugin

try:
    import gouda
    from gouda.engines import InliteEngine, LibDMTXEngine, ZbarEngine
    from gouda.strategies.roi.roi import roi
    from gouda.strategies.resize import resize
except ImportError:
    gouda = None



class BarcodePlugin(Plugin):
    NAME = 'Read barcodes'
    DESCRIPTION = ("Will load the full-resolution scanned image and will set "
                   "each box's 'catalogNumber' metadata field with value(s) of "
                   "any barcodes.")

    def __init__(self, document, parent):
        super(BarcodePlugin, self).__init__()
        if not gouda:
            raise InselectError('Barcode decoding is not available')
        else:
            self.document = document

    @classmethod
    def icon(cls):
        return QIcon(':/data/barcode_icon.png')

    def __call__(self, progress):
        debug_print('BarcodePlugin.__call__')

        engine = _load_engine()

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
                item['fields']['catalogNumber'] = barcodes
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


def _load_engine():
    """Returns the user's choice of barcode reading engine
    """
    s = QSettings()
    engine = s.value("barcode/engine", "libdmtx")
    if 'libdmtx' == engine:
        return LibDMTXEngine()
    elif 'zbar' == engine:
        return ZbarEngine()
    elif 'inlite' == engine:
        format = s.value("barcode/format", "datamatrix")
        return InliteEngine(format)
    else:
        raise ValueError('Unrecognised barcode reader [{0}]'.format(engine))
