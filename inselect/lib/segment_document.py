from .rect import Rect
from .segment import segment_edges, segment_grabcut
from .sort_document_items import sort_document_items
from .utils import debug_print

SEGMENTATION_PREFERRED_WIDTH = 4096


class SegmentDocument(object):
    """Segments and sub-segments documents, applies padding to rects
    and orders rects.
    """
    def __init__(self, sort_by_columns=False):
        self.sort_by_columns = sort_by_columns

    def segment(self, doc, resize=None, *args, **kwargs):
        """Returns doc with items replaced by the result of calling segment_edges().
        The caller is responsible for saving doc.
        """
        debug_print('Segmenting [{0}]'.format(doc))

        # Document promises that either the thumbnail or scanned image will be
        # available
        if doc.thumbnail.available:
            img = doc.thumbnail
            debug_print('Will segment using thumbnail [{0}]'.format(img))
        else:
            img = doc.scanned
            debug_print('Will segment using full-res scan [{0}]'.format(img))

        # Make smaller images larger
        height, width = img.array.shape[:2]
        if resize is None and width != SEGMENTATION_PREFERRED_WIDTH:
            # Resize, maintaining aspect ratio
            # segment_edges() expects a tuple (height, width)
            factor = float(SEGMENTATION_PREFERRED_WIDTH) / width
            resize = (int(height * factor), SEGMENTATION_PREFERRED_WIDTH)

            msg = 'Resizing [{0}] from [{1}] to preferred size of [{2}]'
            debug_print(msg.format(doc, (height, width), resize))
        else:
            # Images of the preferred size or larger do not need resizing
            debug_print('Image is of the preferred size or larger')
            resize = False

        rects, display_image = segment_edges(
            img.array, resize=resize, *args, **kwargs
        )

        rects = self._post_process_rects(img, rects)

        # Create item dicts
        items = [{"fields": {}, 'rect': r, 'rotation': 0} for r in rects]

        # Sort items by user's most recent preference
        items = sort_document_items(items, self.sort_by_columns)

        doc = doc.copy()    # Deep copy to avoid altering argument
        doc.set_items(items)

        debug_print('Segmented [{0}]'.format(doc))

        return doc, display_image

    def subsegment(self, doc, row, seeds, *args, **kwargs):
        """seeds - a list of tuples (x, y) with coordinates relative to
        the top-left of the sub-segmentation window
        """
        import numpy as np

        # Document promises that either the thumbnail or scanned image will be
        # available
        if doc.thumbnail.available:
            debug_print('Subsegment will work on thumbnail')
            img = doc.thumbnail
        else:
            debug_print('Segment will work on full-res scan')
            img = doc.scanned

        items = doc.items
        window = next(img.from_normalised([items[row]['rect']]))
        rects, display = segment_grabcut(img.array, window, seeds)

        rects = list(self._post_process_rects(img, rects))

        # Copy any existing metadata, rotation etc to the new items, update with
        # new rects and replace the existing item
        existing = items[row]
        new_items = [None] * len(rects)
        for index, rect in enumerate(rects):
            new_items[index] = existing.copy()
            new_items[index]['rect'] = rect

        # Sort items by user's most recent preference
        new_items = sort_document_items(new_items, self.sort_by_columns)

        items[row:(1+row)] = new_items

        # Segmentation image
        h, w = img.array.shape[:2]
        display_image = np.zeros((h, w, 3), dtype=np.uint8)

        x, y, w, h = window
        display_image[y:y+h, x:x+w] = display

        return items, display_image

    def _post_process_rects(self, img, rects):
        """Generator of instances of normalised Rect with padding applied
        """
        # Normalised coords and construct instances of Rect
        rects = list(Rect(*map(lambda v: int(round(v)), rect[:4])) for rect in rects)
        rects = img.to_normalised(rects)

        # Apply padding of one percent of height and width
        rects = (r.padded(percent=1) for r in rects)

        # Constrain rects to be within image
        return (r.intersect(Rect(0.0, 0.0, 1.0, 1.0)) for r in rects)
