from PySide.QtGui import QMessageBox

from inselect.lib.segment_document import SegmentDocument
from inselect.lib.utils import debug_print

from inselect.gui.sort_document_items import sort_items_choice
from inselect.gui.utils import load_icon

from .plugin import Plugin


class SubsegmentPlugin(Plugin):
    NAME = 'Subsegment box'
    DESCRIPTION = ('Will subsegment and replace the selected box using seed '
                   'points.')

    def __init__(self, document, parent):
        super(SubsegmentPlugin, self).__init__()
        self.rects = self.display = None
        self.document = document
        self.parent = parent
        self.sort_choice = sort_items_choice().by_columns

    @classmethod
    def icon(cls):
        return load_icon(':/icons/subsegment.png')

    def can_be_run(self):
        selected = self.parent.view_object.selectedIndexes()
        items_of_indexes = self.parent.view_graphics_item.items_of_indexes
        item = items_of_indexes(selected).next() if 1 == len(selected) else None
        seeds = item.points_of_interest if item else None

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
        debug_print('SubsegmentPlugin.__call__')

        # Points as a list of tuples, with coordinates relative to
        # the top-left of the sub-segmentation window
        seeds = [(int(p.x()), int(p.y())) for p in self.seeds]

        items, display_image = SegmentDocument(self.sort_choice).subsegment(
            self.document, self.row, seeds, callback=progress
        )

        self.items, self.display = items, display_image

        debug_print(
            'SegmentPlugin.__call__ exiting. Found [{0}] boxes'.format(len(items))
        )
