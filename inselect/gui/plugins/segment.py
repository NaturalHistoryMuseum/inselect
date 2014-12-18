from pathlib import Path

from PySide.QtGui import QIcon, QMessageBox

from inselect.lib.inselect_error import InselectError
from inselect.lib.segment import segment_edges
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
        dir = Path(__file__).resolve().parents[3]
        return QIcon(str(dir / 'data' / 'segment_icon.png'))

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
        if self.document.thumbnail:
            debug_print('Segment will work on thumbnail')
            image = self.document.thumbnail
        else:
            debug_print('Segment will work on full-res scan')
            image = self.document.scanned
        rects, display = segment_edges(image.array,
                                       window=None,
                                       resize=(5000, 5000),
                                       variance_threshold=100,
                                       size_filter=1,
                                       callback=progress)

        # Reverse order so that boxes at the top left are towards the start
        # and boxes at the bottom right are towards the end
        rects = [{'rect': r} for r in image.to_normalised(list(reversed(rects)))]

        self.items, self.display = rects, display

        debug_print('SegmentPlugin.__call__ exiting. Found [{0}] boxes'.format(len(rects)))
