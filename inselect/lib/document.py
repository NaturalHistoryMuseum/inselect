import json
import shutil
import tempfile

from copy import deepcopy
from itertools import izip, count
from pathlib import Path

import cv2

from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print
from inselect.lib.rect import Rect


def validate_normalised(boxes):
    for l,t,w,h in boxes:
        if not (l>=0 and t>=0 and l<=1 and t<=1 and w>0 and l+w<=1 and h>0 and
                t+h<=1):
            raise InselectError('One or more boxes are not normalised')


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

    def crops(self, normalised):
        "Iterate over crops."
        for box in self.from_normalised(normalised):
            x0, y0, x1, y1 = box.coordinates
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


class InselectDocument(object):
    """Simple represention of an Inselect document
    """

    VERSION = 1
    EXTENSION = '.inselect'

    # TODO LH __eq__, __ne__?
    # TODO LH Store Rect instances within items
    # TODO LH Validate rotation?

    def __init__(self, scanned, items):
        items = self._preprocess_items(items)
        validate_normalised([i['rect'] for i in items])

        self.scanned = InselectImage(scanned)

        thumbnail = self._thumbnail_path()
        self.thumbnail = InselectImage(thumbnail) if thumbnail.is_file() else None

        self._items = items

    def __repr__(self):
        s = "InselectDocument ['{0}'] [{1} items]"
        return s.format(str(self.scanned.path), len(self._items))

    def _thumbnail_path(self):
        return self.scanned.path.parent / (self.scanned.path.stem + '_thumbnail.jpg')

    @property
    def document_path(self):
        return self.scanned.path.with_suffix(self.EXTENSION)

    @property
    def crops_dir(self):
        return self.scanned.path.parent / (self.scanned.path.stem + '_crops')

    @property
    def items(self):
        "Returns a list of dicts of items"
        return deepcopy(self._items)

    def set_items(self, items):
        "Replace self.items with items"
        items = deepcopy(items)
        items = self._preprocess_items(items)
        # TODO Validate metadata
        validate_normalised(i['rect'] for i in items)
        self._items = items

    def _preprocess_items(self, items):
        # Returns items with tuples of boxes replaced with Rect instances
        for i in xrange(0, len(items)):
            l,t,w,h = items[i]['rect']
            items[i]['rect'] = Rect(l,t,w,h)
        return items

    @classmethod
    def new_from_scan(cls, scanned):
        "Creates, saves and returns a new InselectDocument on the scanned image"
        # TODO LH Raise error if a thumbnail image is ingested
        scanned = Path(scanned)
        if not scanned.is_file():
            raise InselectError('Image file [{0}] does not exist'.format(scanned))
        else:
            debug_print('Creating on image [{0}]'.format(scanned))
            doc = InselectDocument(scanned, items=[])
            if doc.document_path.is_file():
                raise InselectError('Document file [{0}] already exists'.format(doc.document_path))
            else:
                doc.save()
                return doc

    @classmethod
    def load(cls, path):
        "Returns a new InselectDocument"
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
        "Saves to self.document_path"
        # TODO LH Clear existing crops dir?
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

    @property
    def crops(self):
        "Iterate over cropped specimen image arrays"
        return self.scanned.crops([i['rect'] for i in self.items])

    def save_crops_from_image(self, dir, image, progress=None):
        "Saves images cropped from image to dir. dir must exist."
        boxes = [i['rect'] for i in self.items]
        template = '{0:03}' + image.path.suffix
        paths = [dir / template.format(1+i) for i in xrange(0, len(self.items))]
        image.save_crops(boxes, paths, progress)

    def save_crops(self, progress=None):
        "Saves images cropped from self.scanned to self.crops_dir"
        # TODO LH Test that cancel of export leaves existing crops dir.
        # Create temp dir alongside scan
        tempdir = tempfile.mkdtemp(dir=str(self.scanned.path.parent),
            prefix=self.scanned.path.stem + '_temp_crops')
        tempdir = Path(tempdir)
        debug_print('Saving crops to to temp dir [{0}]'.format(tempdir))
        try:
            # Save crops
            self.save_crops_from_image(tempdir, self.scanned, progress)

            # rm existing crops dir
            crops_dir = self.crops_dir
            shutil.rmtree(str(crops_dir), ignore_errors=True)

            # Rename temp dir
            tempdir.rename(crops_dir)
            tempdir = None

            debug_print('Saved [{0}] crops to [{1}]'.format(len(self.items), crops_dir))

            return crops_dir
        finally:
            if tempdir:
                shutil.rmtree(str(tempdir))

    def ensure_thumbnail(self, width=4096):
        if self.thumbnail is None:
            p = self._thumbnail_path()

            # File might have been created after this instance
            if not p.is_file():
                debug_print('Creating [{0}] with width of [{1}] pixels'.format(p, width))
                # TODO LH Sensible limits?
                # TODO LH What if self.scanned.width<width?
                min, max = 512, 8192
                if not min<width<max:
                    raise InselectError('width should be between [{0}] and [{1}]'.format(min, max))
                else:
                    img = self.scanned.array
                    factor  = float(width)/img.shape[1]
                    debug_print('Resizing to [{0}] pixels wide'.format(width))
                    thumbnail = cv2.resize(img, (0,0), fx=factor, fy=factor)
                    debug_print('Writing to [{0}]'.format(p))
                    # TODO Copy EXIF tags?
                    res = cv2.imwrite(str(p), thumbnail)
                    if not res:
                        raise InselectError('Unable to write thumbnail [{0}]'.format(p))

            # Load it
            self.thumbnail = InselectImage(p)
