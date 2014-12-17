import json
import shutil
import tempfile

from copy import deepcopy
from pathlib import Path

import cv2

from inselect.lib.image import InselectImage
from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print, validate_normalised
from inselect.lib.rect import Rect


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

        self._scanned = InselectImage(scanned)

        thumbnail = self._thumbnail_path()
        self._thumbnail = InselectImage(thumbnail) if thumbnail.is_file() else None

        self._items = items

    def __repr__(self):
        s = "InselectDocument ['{0}'] [{1} items]"
        return s.format(str(self._scanned.path), len(self._items))

    def _thumbnail_path(self):
        return self._scanned.path.parent / (self._scanned.path.stem + '_thumbnail.jpg')

    @property
    def scanned(self):
        return self._scanned

    @property
    def thumbnail(self):
        return self._thumbnail

    @property
    def document_path(self):
        return self._scanned.path.with_suffix(self.EXTENSION)

    @property
    def crops_dir(self):
        return self._scanned.path.parent / (self._scanned.path.stem + '_crops')

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
                'scanned extension': self._scanned.path.suffix,
                'items' : items,
              }

        json.dump(doc, open(str(path), "w"), indent=4)

        debug_print('Saved [{0}] items to [{1}]'.format(len(items), path))

    @property
    def crops(self):
        "Iterate over cropped specimen image arrays"
        return self._scanned.crops([i['rect'] for i in self.items])

    def save_crops_from_image(self, dir, image, progress=None):
        "Saves images cropped from image to dir. dir must exist."
        boxes = [i['rect'] for i in self.items]
        template = '{0:03}' + image.path.suffix
        paths = [dir / template.format(1+i) for i in xrange(0, len(self.items))]
        image.save_crops(boxes, paths, progress)

    def save_crops(self, progress=None):
        "Saves images cropped from self._scanned to self.crops_dir"
        # TODO LH Test that cancel of export leaves existing crops dir.
        # Create temp dir alongside scan
        tempdir = tempfile.mkdtemp(dir=str(self._scanned.path.parent),
            prefix=self._scanned.path.stem + '_temp_crops')
        tempdir = Path(tempdir)
        debug_print('Saving crops to to temp dir [{0}]'.format(tempdir))
        try:
            # Save crops
            self.save_crops_from_image(tempdir, self._scanned, progress)

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
        if self._thumbnail is None:
            p = self._thumbnail_path()

            # File might have been created after this instance
            if not p.is_file():
                debug_print('Creating [{0}] with width of [{1}] pixels'.format(p, width))
                # TODO LH Sensible limits?
                # TODO LH What if self._scanned.width<width?
                min, max = 512, 8192
                if not min<width<max:
                    raise InselectError('width should be between [{0}] and [{1}]'.format(min, max))
                else:
                    img = self._scanned.array
                    factor  = float(width)/img.shape[1]
                    debug_print('Resizing to [{0}] pixels wide'.format(width))
                    thumbnail = cv2.resize(img, (0,0), fx=factor, fy=factor)
                    debug_print('Writing to [{0}]'.format(p))
                    # TODO Copy EXIF tags?
                    res = cv2.imwrite(str(p), thumbnail)
                    if not res:
                        raise InselectError('Unable to write thumbnail [{0}]'.format(p))

            # Load it
            self._thumbnail = InselectImage(p)
