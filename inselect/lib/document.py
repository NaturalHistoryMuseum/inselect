import json
import shutil
import tempfile

from copy import deepcopy
from itertools import izip
from pathlib import Path

import cv2

from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print
from inselect.lib.rect import Rect


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

    def __repr__(self):
        return "InselectImage('{0}')".format(str(self._path))

    def __str__(self):
        loaded = 'Unloaded' if self._npimage is None else 'Loaded'
        return "InselectImage ['{0}'] [{1}]".format(str(self._path), loaded)

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
            yield Rect(int(w*left), int(h*top), int(w*width), int(h*height))

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
            yield Rect(float(left)/w, float(top)/h, float(width)/w,
                       float(height)/h)

    def save_crops(self, normalised, paths):
        for box,path in izip(self.from_normalised(normalised), paths):
            x0, y0, x1, y1 = box.coordinates
            cv2.imwrite(str(path), self.array[y0:y1, x0:x1])
            debug_print('Wrote [{0}]'.format(path))


class InselectDocument(object):
    """Simple represention of an Inselect document
    """

    VERSION = 1

    # TODO LH repr
    # TODO LH str
    # TODO LH __eq__, __ne__?
    # TODO LH Store Rect instances within items

    def __init__(self, scanned, items):
        items = self._preprocess_items(items)
        validate_normalised([i['rect'] for i in items])

        self.scanned = InselectImage(scanned)

        thumbnail = scanned.parent / (scanned.stem + '_thumbnail.jpg')
        self.thumbnail = InselectImage(thumbnail) if thumbnail.is_file() else None

        self._items = items

    def __repr__(self):
        s = "InselectDocument ['{0}'] [{1} items]"
        return s.format(str(self.scanned.path), len(self._items))

    @property
    def document_path(self):
        return self.scanned.path.with_suffix('.inselect')

    @property
    def crops_dir(self):
        return self.scanned.path.parent / (self.scanned.path.stem + '_crops')

    @property
    def items(self):
        return self._items

    def set_items(self, items):
        items = deepcopy(items)
        items = self._preprocess_items(items)
        validate_normalised(i['rect'] for i in items)
        self._items = items

    def _preprocess_items(self, items):
        # Returns items with tuples of boxes replaced with Rect instances
        for i in xrange(0, len(items)):
            l,t,w,h = items[i]['rect']
            items[i]['rect'] = Rect(l,t,w,h)
        return items

    @classmethod
    def load(cls, path):
        debug_print('Loading from [{0}]'.format(path))

        path = Path(path)
        doc = json.load(path.open())

        v = doc.get('inselect version')
        if not v:
            raise InselectError('Not an inselect document')
        elif v > cls.VERSION:
            raise InselectError('Unsupported version [{0}]'.format(v))

        scanned = path.with_suffix(doc['scanned extension'])

        debug_print('Loaded [{0}] items from [{1}]'.format(len(doc['items']), path))

        return InselectDocument(scanned, doc['items'])

    def save(self):
        path = self.document_path
        debug_print('Saving [{0}] items to [{1}]'.format(len(self._items), path))

        # Convert Rect instances to lists
        items = deepcopy(self._items)
        for i in xrange(0, len(items)):
            l,t,w,h = items[i]['rect']
            items[i]['rect'] = [l,t,w,h]

        doc = { 'inselect version': self.VERSION,
                'scanned extension': self.scanned.path.suffix,
                'items' : items,
              }

        json.dump(doc, open(str(path), "w"), indent=4)

        debug_print('Saved [{0}] items to [{1}]'.format(len(items), path))

    def save_crops(self, crop_ext='.tiff'):
        # TODO LH Take a progress function, which will be passed a number 
        #          between 0 and 100. Function can raise an exception to cancel
        #          export.
        # TODO LH Test that cancel of export leaves existing crops dir.

        # Create temp dir alongside scan
        tempdir = tempfile.mkdtemp(dir=str(self.scanned.path.parent),
            prefix=self.scanned.path.stem + '_temp_crops')
        tempdir = Path(tempdir)
        debug_print('Saving crops to to temp dir [{0}]'.format(tempdir))
        try:
            # Save crops
            boxes = [i['rect'] for i in self.items]
            template = '{0:03}' + crop_ext
            paths = [tempdir / template.format(1+i) for i in xrange(0, len(self.items))]
            self.scanned.save_crops(boxes, paths)

            # rm existing crops dir
            crops_dir = self.crops_dir
            shutil.rmtree(str(crops_dir), ignore_errors=True)

            # Rename temp dir
            tempdir.rename(crops_dir)
            tempdir = None

            debug_print('Saved [{0}] crops to [{1}]'.format(len(boxes), crops_dir))

            return crops_dir
        finally:
            if tempdir:
                shutil.rmtree(str(tempdir))
