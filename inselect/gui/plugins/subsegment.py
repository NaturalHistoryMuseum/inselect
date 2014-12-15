from pathlib import Path

import numpy as np

from PySide.QtGui import QIcon

from inselect.lib.inselect_error import InselectError
from inselect.lib.segment import segment_grabcut
from inselect.lib.utils import debug_print

from .plugin import Plugin


class SubsegmentPlugin(Plugin):
    def __init__(self, app):
        self.rects = self.display = None

        # TODO LH Fix this horrible, horrible, horrible, horrible, horrible hack
        selected = app.view_grid.selectedIndexes()
        items_of_indexes = app.view_graphics_item.items_of_indexes
        item = items_of_indexes(selected).next() if 1 == len(selected) else None
        seeds = item.subsegmentation_seed_points if item else None

        if not seeds or len(seeds) < 2:
            raise ValueError('Please select exactly one box and that contains '
                             'at least two seed points')
        else:
            self.row = selected[0].row()
            self.seeds = seeds

    @classmethod
    def name(cls):
        """Name of the plugin
        """
        return 'Subsegment box'

    @classmethod
    def prompt(cls):
        """A description of the effect of running this plugin.
        """
        return ('Subsegmenting will replace the selected box.')

    @classmethod
    def icon(cls):
        dir = Path(__file__).resolve().parents[3]
        return QIcon(str(dir / 'data' / 'subsegment_icon.png'))

    def __call__(self, document, progress):
        """
        """
        debug_print('SubsegmentPlugin.__call__')

        if document.thumbnail:
            debug_print('Subsegment will work on thumbnail')
            image = document.thumbnail
        else:
            debug_print('Segment will work on full-res scan')
            image = document.scanned

        # Perform the subsegmentation
        items = document.items
        row = self.row
        window = image.from_normalised([items[row]['rect']]).next()

        # Seed points as a list of tuples, with coordinates relative to
        # the top-left of the sub-segmentation window
        seeds = [(p.x()-window.left, p.y()-window.top) for p in self.seeds]

        rects, display = segment_grabcut(image.array, window, seeds)

        # Replace the item
        rects = [{'rect': r} for r in image.to_normalised(rects)]
        items[row:(1+row)] = rects

        # Segmentation image
        h, w = image.array.shape[:2]
        display_image = np.zeros((h, w, 3), dtype=np.uint8)

        x, y, w, h = window
        display_image[y:y+h, x:x+w] = display

        self.items, self.display = items, display_image

        debug_print('SegmentPlugin.__call__ exiting. Found [{0}] boxes'.format(len(rects)))
