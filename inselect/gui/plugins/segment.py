from PyQt5.QtWidgets import QMessageBox

from inselect.lib.segment_document import SegmentDocument
from inselect.lib.utils import debug_print

from inselect.gui.sort_document_items import sort_items_choice
from inselect.gui.utils import load_icon

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
        self.sort_choice = sort_items_choice().by_columns

    @classmethod
    def icon(cls):
        return load_icon(':/icons/segment.png')

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
        doc, display = SegmentDocument(self.sort_choice).segment(
            self.document, callback=progress
        )

        self.items, self.display = doc.items, display

        debug_print('SegmentPlugin.__call__ exiting. Found [{0}] boxes'.format(
            len(self.items))
        )
