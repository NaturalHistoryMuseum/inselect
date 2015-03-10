from pathlib import Path

import numpy as np

from PySide.QtGui import QIcon, QMessageBox

from inselect.gui import icons
from inselect.lib.inselect_error import InselectError
from inselect.lib.segment import segment_grabcut
from inselect.lib.utils import debug_print

from .plugin import Plugin


class SubsegmentPlugin(Plugin):
    def __init__(self, document, parent):
        self.rects = self.display = None
        self.document = document
        self.parent = parent

    @classmethod
    def name(cls):
        """Name of the plugin
        """
        return 'Subsegment box'

    @classmethod
    def description(cls):
        """A description of the effect of running this plugin.
        """
        return ('Will subsegment and replace the selected box using seed '
                'points.')

    @classmethod
    def icon(cls):
        return QIcon(':/data/subsegment_icon.png')

    def proceed(self):
        # TODO LH Fix this horrible, horrible, horrible, horrible, horrible hack
        selected = self.parent.view_specimen.selectedIndexes()
        items_of_indexes = self.parent.view_graphics_item.items_of_indexes
        item = items_of_indexes(selected).next() if 1 == len(selected) else None
        seeds = item.subsegmentation_seed_points if item else None

        if not seeds or len(seeds) < 2:
            msg = ('Please select exactly one box that contains at least two '
                   'seed points')
            QMessageBox.warning(self.parent, "Unable to subsegment", msg)
            return False
        else:
            self.row = selected[0].row()
            self.seeds = seeds
            return True

    def __call__(self, progress):
        """
        """
        debug_print('SubsegmentPlugin.__call__')

        if self.document.thumbnail:
            debug_print('Subsegment will work on thumbnail')
            image = self.document.thumbnail
        else:
            debug_print('Segment will work on full-res scan')
            image = self.document.scanned

        # Perform the subsegmentation
        items = self.document.items
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
