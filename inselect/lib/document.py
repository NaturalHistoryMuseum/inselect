import json
import re
import shutil
import tempfile

from copy import deepcopy
from pathlib import Path

import cv2

from .image import InselectImage
from .inselect_error import InselectError
from .unicode_csv import UnicodeWriter
from .utils import debug_print, validate_normalised
from .rect import Rect


class InselectDocument(object):
    """Simple represention of an Inselect document.

    You should probably create instances using the class methods new_from_scan
    or load.
    """

    VERSION = 1
    EXTENSION = '.inselect'
    THUMBNAIL_SUFFIX = '_thumbnail.jpg'

    # A temporary solution to metadata fields
    METADATA_FIELDS = ('Specimen number', 'Location', 'Taxonomic group',)

    # TODO LH __eq__, __ne__?
    # TODO LH Store Rect instances within items
    # TODO LH Validate rotation?

    def __init__(self, scanned=None, scanned_path=None, thumbnail=None,
                 items=[]):
        """
        """
        items = self._preprocess_items(items)

        # TODO Validate metadata
        validate_normalised([i['rect'] for i in items])

        self._scanned = scanned if scanned else InselectImage(scanned_path)

        if thumbnail:
            self._thumbnail = thumbnail
        else:
            t = self.thumbnail_path_of_scanned(self._scanned.path)
            self._thumbnail = InselectImage(t) if t.is_file() else None

        self._items = items

    @classmethod
    def document_path_of_scanned(cls, scanned):
        """Returns the path of the document for the given scanned image
        """
        scanned = Path(scanned)
        return scanned.parent / (scanned.stem + cls.EXTENSION)

    @classmethod
    def document_path_of_thumbnail(cls, thumbnail):
        """Returns the path of the document for the given thumbnail image
        """
        thumbnail = Path(thumbnail)
        fname = thumbnail.name.replace(cls.THUMBNAIL_SUFFIX, cls.EXTENSION)
        return thumbnail.parent / fname

    @classmethod
    def thumbnail_path_of_scanned(cls, scanned):
        """Returns the path of the thumbnail image for the given scanned image
        """
        scanned = Path(scanned)
        return scanned.parent / (scanned.stem + cls.THUMBNAIL_SUFFIX)

    def copy(self):
        """Returns a new instance of InselectDocument that is a copy of this
        instance
        """
        return InselectDocument(scanned=self.scanned,
                                thumbnail=self.thumbnail,
                                items=self.items)

    def __repr__(self):
        s = "InselectDocument ['{0}'] [{1} items]"
        return s.format(str(self._scanned.path), len(self._items))

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

    @property
    def n_items(self):
        return len(self._items)

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
            doc = cls(scanned_path=scanned, items=[])
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

        # Sniff the first few bytes - file must look like a json document
        if not re.match('{[ \n]*"', path.open('rb').read(20)):
            raise InselectError('Not an inselect document')
        else:
            doc = json.load(path.open())
            v = doc.get('inselect version')
            if not v:
                raise InselectError('Not an inselect document')
            elif v > cls.VERSION:
                raise InselectError('Unsupported version [{0}]'.format(v))
            else:
                scanned = path.with_suffix(doc['scanned extension'])

                msg = 'Loaded [{0}] items from [{1}]'
                debug_print(msg.format(len(doc['items']), path))

                return cls(scanned_path=scanned, items=doc['items'])

    def save(self):
        "Saves to self.document_path"
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

        # Specify separators to prevent trailing whitespace
        json.dump(doc, open(str(path), "w"), indent=4, separators=(',', ': '))

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
            debug_print('Moving temp crops dir [{0}] to [{1}]'.format(tempdir, crops_dir))
            tempdir.rename(crops_dir)
            tempdir = None

            debug_print('Saved [{0}] crops to [{1}]'.format(len(self.items), crops_dir))

            return crops_dir
        finally:
            if tempdir:
                shutil.rmtree(str(tempdir))

    def ensure_thumbnail(self, width=4096):
        if self._thumbnail is None:
            p = self.thumbnail_path_of_scanned(self._scanned.path)

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

    @property
    def metadata_fields(self):
        """An iterable of metadata field names
        """
        # Temporary solution
        return self.METADATA_FIELDS

    def export_csv(self, path):
        fields = self.metadata_fields
        with Path(path).open('wb') as f:
            w = UnicodeWriter(f)
            w.writerow(('Item',) + fields)
            for index,item in enumerate(self._items):
                w.writerow([1+index] + [item['fields'].get(f) for f in fields])
