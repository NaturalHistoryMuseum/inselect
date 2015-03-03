from itertools import izip, count
from pathlib import Path

import cv2
import numpy as np

from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print
from inselect.lib.rect import Rect


class InselectImage(object):
    """Simple representation of an inselect image
    """

    # TODO LH __eq__, __ne__?

    def __init__(self, path):
        path = Path(path)
        if not path.is_file():
            raise InselectError('Image file [{0}] does not exist'.format(str(path)))
        else:
            self._path = path
            self._array = None

    def __repr__(self):
        return "InselectImage('{0}')".format(str(self._path))

    def __str__(self):
        loaded = 'Unloaded' if self._array is None else 'Loaded'
        return "InselectImage ['{0}'] [{1}]".format(str(self._path), loaded)

    @property
    def path(self):
        return self._path

    @property
    def array(self):
        """ Lazy-load np.array of the image
        """
        if self._array is None:
            p = str(self._path)
            debug_print('Reading from image file [{0}]'.format(p))
            image = cv2.imread(p)
            if image is None:
                raise InselectError('[{0}] could not be read as an image'.format(p))
            else:
                self._array = image
        return self._array

    def from_normalised(self, boxes):
        h, w = self.array.shape[:2]
        for left, top, width, height in boxes:
            yield Rect(int(w*left), int(h*top), int(w*width), int(h*height))

    def to_normalised(self, boxes):
        h, w = self.array.shape[:2]
        for left, top, width, height in boxes:
            yield Rect(float(left)/w, float(top)/h, float(width)/w,
                       float(height)/h)

    def crops(self, normalised):
        "Iterate over crops."
        # TODO LH Fill back if not in self.array.shape[:2]
        w, h = self.array.shape[:2]
        for box in self.from_normalised(normalised):
            x0, y0, x1, y1 = box.coordinates
            if 0 <= x0 <= w and 0 <= y0 <= h and 0 <= x1 <= w and 0 <= y1 <= h:
                # View
                yield self.array[y0:y1, x0:x1]
            else:
                # TODO LH Create new array and fill. Transparency?
                yield self.array[y0:y1, x0:x1]

    def save_crops(self, normalised, paths, progress=None):
        "Saves crops given in normalised to paths."
        # TODO Copy EXIF tags?
        # TODO Make read-only?
        for index, crop, path in izip(count(), self.crops(normalised), paths):
            if progress:
                progress('Writing crop {0}'.format(1 + index))
            if not cv2.imwrite(str(path), crop):
                raise InselectError('Unable to write crop [{0}]'.format(path))
            else:
                debug_print('Wrote crop [{0}]'.format(path))
