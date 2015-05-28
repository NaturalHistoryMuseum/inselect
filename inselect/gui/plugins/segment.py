from PySide.QtGui import QIcon, QMessageBox

from inselect.lib.segment import segment_document
from inselect.lib.utils import debug_print

from .plugin import Plugin


class SegmentPlugin(Plugin):
    NAME = 'Segment image'
    DESCRIPTION = ('Will segment the image, replacing all existing boxes and '
                   'metadata.')

    def __init__(self, document, parent):
        super(SegmentPlugin, self).__init__()
        self.rects = self.display = None
        self.document = document
        self.parent = parent

    @classmethod
    def icon(cls):
        return QIcon(':/data/segment_icon.png')

    def can_be_run(self):
        if self.document.items:
            msg = ('Segmenting will cause all boxes and metadata to be '
                   'replaced.\n\nContinue and replace all existing '
                   'boxes and metadata')
            res = QMessageBox.question(self.parent, 'Replace boxes?', msg,
                                       QMessageBox.No, QMessageBox.Yes)
            return QMessageBox.Yes == res
        else:
            return True

    def __call__(self, progress):
        debug_print('SegmentPlugin.__call__')
        doc, display = segment_document(self.document, callback=progress)

        self.items, self.display = doc.items, display

        debug_print('SegmentPlugin.__call__ exiting. Found [{0}] boxes'.format(len(self.items)))
