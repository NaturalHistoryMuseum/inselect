import warnings

from itertools import izip, count, chain, repeat
from pathlib import Path

import cv2
import numpy as np

from PIL import Image

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
        """Lazy-load np.array of the colour image array, with channels stored in
        order B G R
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
        """Generator function that yields instances of Rect
        """
        w, h = self.dimensions
        for left, top, width, height in boxes:
            yield Rect(int(w*left), int(h*top), int(w*width), int(h*height))

    def to_normalised(self, boxes):
        """Generator function that yields instances of Rect
        """
        w, h = self.dimensions
        for left, top, width, height in boxes:
            yield Rect(float(left)/w, float(top)/h, float(width)/w,
                       float(height)/h)

    def crops(self, normalised, rotation=None):
        """Generator function that yields cropped images
        Rotation should be None, an int or an iterable. If not None, crops will
        be rotated by that many clockwise degrees.
        """

        if not rotation:
            rotation = repeat(0)
        elif isinstance(rotation, (int, long)):
            rotation = repeat(rotation)

        h, w = self.array.shape[:2]
        for box, rotate in izip(self.from_normalised(normalised), rotation):
            x0, y0, x1, y1 = box.coordinates
            x_in_bounds = [0 <= x0 <= w, 0 <= x1 <= w]
            y_in_bounds = [0 <= y0 <= h, 0 <= y1 <= h]
            if all(chain(x_in_bounds, y_in_bounds)):
                # View
                crop = self.array[y0:y1, x0:x1]
            else:
                # Box is out of bounds -create a new array, all zeroes (black)
                crop_w, crop_h = x1-x0, y1-y0
                crop = np.zeros((crop_h, crop_w, self.array.shape[2]),
                                dtype=self.array.dtype)
                if any(x_in_bounds) and any(y_in_bounds):
                    # Partial overlap
                    overlapping = self.array[max(y0, 0):min(y1, h),
                                             max(x0, 0):min(x1, w)]
                    dest_y, dest_x = max(0, 0-y0), max(0, 0-x0)
                    crop[dest_y:(dest_y + overlapping.shape[0]),
                         dest_x:(dest_x + overlapping.shape[1])] = overlapping

            if 0 != rotate % 90:
                msg = 'Rotation is not a multiple of 90: [{0}]'
                raise ValueError(msg.format(rotate))
            else:
                n_rotations = (rotate % 360) / 90
                # n_rotations will be 0, 1, 2 or 3 = the number of 90 degree
                # clockwise rotations
                if 1 == n_rotations:
                    # Rotate 90 clockwise
                    crop = cv2.flip(cv2.transpose(crop), 1)
                elif 2 == n_rotations:
                    # Rotate 180 clockwise
                    crop = cv2.flip(crop, -1)
                elif 3 == n_rotations:
                    # Rotate 90 counter-clockwise
                    crop = cv2.flip(cv2.transpose(crop), 0)

            yield crop

    def save_crops(self, normalised, paths, rotation=None, progress=None):
        """Saves crops given in normalised to paths.
        Rotation should be the number of clockwise degrees by which the crops
        should be rotated.
        """
        # TODO Copy EXIF tags?
        # TODO Make read-only?
        for index, crop, path in izip(count(), self.crops(normalised, rotation), paths):
            if progress:
                progress('Writing crop {0}'.format(1 + index))
            if not cv2.imwrite(str(path), crop):
                raise InselectError('Unable to write crop [{0}]'.format(path))
            else:
                debug_print('Wrote crop [{0}]'.format(path))

    @property
    def size_bytes(self):
        "The integer size of this file in bytes"
        return self._path.stat().st_size

    @property
    def pil_image(self):
        "Returns a PIL.Image instance represention"
        with warnings.catch_warnings(), self._path.open('rb') as f:
            # Ignore DecompressionBombWarning - expect images to be > 89478485
            # pixels
            warnings.simplefilter("ignore", Image.DecompressionBombWarning)
            return Image.open(f)

    @property
    def dimensions(self):
        "A tuple (height, width)"
        if self._array is not None:
            # Get directly from the array
            return self._array.shape[1], self._array.shape[0]
        else:
            return self.pil_image.size
