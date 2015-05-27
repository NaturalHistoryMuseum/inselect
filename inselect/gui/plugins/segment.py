from PySide.QtGui import QIcon, QMessageBox

from inselect.lib.segment import segment_document
from inselect.lib.utils import debug_print

from .plugin import Plugin


class SegmentPlugin(Plugin):
    def __init__(self, document, parent):
        self.rects = self.display = None
        self.document = document
        self.parent = parent

    @classmethod
    def name(cls):
        """Name of the plugin
        """
        return 'Segment image'

    @classmethod
    def description(cls):
        """A description of the effect of running this plugin.
        """
        return ('Will segment the image, replacing all existing boxes and '
                'metadata.')

    @classmethod
    def icon(cls):
        return QIcon(':/data/segment_icon.png')

    def proceed(self):
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
        """
        """
        debug_print('SegmentPlugin.__call__')
        doc, display = segment_document(self.document, callback=progress)

        self.items, self.display = doc.items, display

        debug_print('SegmentPlugin.__call__ exiting. Found [{0}] boxes'.format(len(self.items)))
