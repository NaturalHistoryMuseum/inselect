from itertools import count

from qtpy.QtWidgets import QMessageBox

import inselect.lib.utils

from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print

from inselect.gui.utils import load_icon

from .plugin import Plugin
from .barcode_dialog import BarcodeDialog
from .barcode_settings import load_engine


# Warning: lazy load of gouda via local imports


class BarcodePlugin(Plugin):
    NAME = 'Read barcodes'
    DESCRIPTION = ("Will load the original full-resolution image and will set "
                   "each box's 'catalogNumber' metadata field with value(s) of "
                   "any barcodes.")

    def __init__(self, document, parent):
        super(BarcodePlugin, self).__init__()
        try:
            import gouda.strategies.roi.roi     # noqa
            import gouda.strategies.resize      # noqa
        except ImportError:
            raise InselectError('Barcode decoding is not available')
        else:
            self.document = document
            self.parent = parent

    @classmethod
    def icon(cls):
        return load_icon(':/icons/barcode.png')

    def can_be_run(self):
        if not self.document.scanned.available:
            msg = ('Unable to read barcodes because the original '
                   'full-resolution image file does not exist.')
            QMessageBox.warning(
                self.parent, 'Original full-resolution image file does not exist',
                msg.format(self.document.scanned.path)
            )
            return False
        else:
            return True

    def __call__(self, progress):
        debug_print('BarcodePlugin.__call__')

        engine = load_engine()

        import gouda.util
        gouda.util.DEBUG_PRINT = inselect.lib.utils.DEBUG_PRINT

        progress('Loading full-res image')
        image_array = self.document.scanned.array

        items = self.document.items
        for index, item, crop in zip(count(), items, self.document.crops):
            msg = 'Reading barcodes in box {0} of {1}'.format(1 + index, len(items))
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
        from gouda.strategies.roi.roi import roi
        from gouda.strategies.resize import resize
        for strategy in (resize, roi):
            # TODO LH Must be able to cancel within call to strategy
            progress()
            result = strategy(crop, engine)
            if result:
                strategy, barcodes = result
                return ' '.join(sorted([b.data.decode() for b in barcodes]))
        return None

    @classmethod
    def config(self, parent):
        dlg = BarcodeDialog(parent)
        dlg.exec_()
