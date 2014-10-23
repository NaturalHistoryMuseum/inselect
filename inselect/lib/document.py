import json

from itertools import izip
from pathlib import Path

import cv2

from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print
from inselect.lib.rect import Rect

VERSION = 1

def validate_normalised(boxes):
    # TODO LH raise error on first failure
    for l,t,w,h in boxes:
        if not (l>=0 and t>=0 and l<=1 and t<=1 and w>0 and l+w<=1 and h>0 and
                t+h<=1):
            raise InselectError('One or more boxes are not normalised')


class InselectImage(object):
    """Simple representation of an inselect image
    """

    # TODO LH repr
    # TODO LH str
    # TODO LH __eq__, __ne__?

    def __init__(self, path):
        path = Path(path)
        if not path.is_file():
            raise InselectError('Image file [{0}] does not exist'.format(str(path)))

        self._path = path
        self._npimage = None

    @property
    def path(self):
        return self._path

    @property
    def array(self):
        """ Lazy-load np.array of the image
        """
        if self._npimage is None:
            p = str(self._path)
            debug_print('Reading from image file [{0}]'.format(p))
            image = cv2.imread(p)
            if image is None:
                raise InselectError('[{0}] could not be read as an image'.format(p))
            else:
                self._npimage = image
        return self._npimage

    def from_normalised(self, boxes):
        validate_normalised(boxes)
        h, w = self.array.shape[:2]
        for left, top, width, height in boxes:
            yield Rect(int(w*left), int(h*top), int(w*(left+width)), int(h*(top+height)))

    def validate_in_bounds(self, boxes):
        h, w = self.array.shape[:2]
        for left, top, width, height in boxes:
            if not (left>=0 and top>=0 and left<w and top<h and width>0 and
                    left+width<=w and height>0 and top+height<=h):
                raise InselectError('One or more boxes are not in bounds')

    def to_normalised(self, boxes):
        self.validate_in_bounds(boxes)
        h, w = self.array.shape[:2]
        for left, top, width, height in boxes:
            yield Rect(float(left)/w, float(top)/h, float(left+width)/w,
                       float(top+height)/h)

    def save_crops(self, normalised, paths):
        for box,path in izip(self.from_normalised(normalised), paths):
            x0, y0, x1, y1 = box.coordinates
            cv2.imwrite(str(path), self.array[y0:y1, x0:x1])
            debug_print('Wrote [{0}]'.format(path))


class InselectDocument(object):
    """Simple represention of an Inselect document
    """

    # TODO LH repr
    # TODO LH str
    # TODO LH __eq__, __ne__?
    # TODO LH Store Rects instances within item

    def __init__(self, scanned, thumbnail, items):
        validate_normalised([i['rect'] for i in items])

        self.scanned, self.thumbnail, self.items = scanned, thumbnail, items
        self.modified = False

    def set_items(self, items):
        _validate_boxes(items)
        self.items = items

    @classmethod
    def load(cls, path):
        debug_print('Loading from [{0}]'.format(path))

        path = Path(path)
        doc = json.load(path.open())

        v = doc.get('inselect version')
        if not v:
            raise InselectError('Not an inselect document')
        elif v > VERSION:
            raise InselectError('Unsupported version [{0}]'.format(v))

        scanned = path.parent / (str(path.stem) + doc['scanned extension'])
        scanned = InselectImage(scanned)

        thumbnail = path.parent / (str(path.stem) + '_thumbnail.jpg')
        if thumbnail.is_file():
            thumbnail = InselectImage(thumbnail)
        else:
            thumbnail = None

        debug_print('Loaded [{0}] items from [{1}]'.format(len(doc['items']), path))

        return InselectDocument(scanned, thumbnail, doc['items'])

    def save(self):
        path = self.scanned.path
        path = path.parent / (str(path.stem) + '.inselect')
        debug_print('Saving [{0}] items to [{1}]'.format(len(self.items), path))

        doc = { 'inselect version': VERSION,
                'scanned extension': self.scanned.path.suffix,
                'items' : self.items,
              }

        json.dump(doc, open(str(path), "w"), indent=4)

        debug_print('Saved [{0}] items to [{1}]'.format(len(self.items), path))
