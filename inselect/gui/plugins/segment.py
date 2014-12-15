from pathlib import Path

from PySide.QtGui import QIcon

from inselect.lib.inselect_error import InselectError
from inselect.lib.segment import segment_edges
from inselect.lib.utils import debug_print

from .plugin import Plugin


class SegmentPlugin(Plugin):
    def __init__(self, app):
        self.rects = self.display = None

    @classmethod
    def name(cls):
        """Name of the plugin
        """
        return 'Segment image'

    @classmethod
    def prompt(cls):
        """A description of the effect of running this plugin.
        """
        return ('Segmenting will cause all boxes and metadata to '
                'be replaced.')

    @classmethod
    def icon(cls):
        dir = Path(__file__).resolve().parents[3]
        return QIcon(str(dir / 'data' / 'segment_icon.png'))

    def __call__(self, document, progress):
        """
        """
        debug_print('SegmentPlugin.__call__')
        if document.thumbnail:
            debug_print('Segment will work on thumbnail')
            image = document.thumbnail
        else:
            debug_print('Segment will work on full-res scan')
            image = document.scanned
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
