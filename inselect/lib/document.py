import json
import pytz
import re

from copy import deepcopy
from datetime import datetime
from itertools import chain
from pathlib import Path

from .image import InselectImage
from .inselect_error import InselectError
from .utils import debug_print, user_name
from .rect import Rect

# Warning: lazy load of cv2 via local imports


class InselectDocument(object):
    """An Inselect document.

    scanned_extension :                      File extension of the
                                             full-resolution image.
    items : list of dicts { fields: {k: v},  Metadata. All k and v should be
                                             strings.
                            rotation: int,   Integer that is a multiple of 90.
                            rect: [x,        Normalised (i.e., between 0.0 and
                                   y,        1.0) floats.
                                   width,
                                   height,
                                  ],
                          }

    You should probably create instances using the class methods new_from_scan
    or load.
    """

    FILE_VERSIONS = (1, 2,)
    EXTENSION = '.inselect'

    THUMBNAIL_MIN_WIDTH = 1024
    THUMBNAIL_MAX_WIDTH = 16384
    THUMBNAIL_DEFAULT_WIDTH = 4096
    THUMBNAIL_SUFFIX = '_thumbnail.jpg'

    # Matches filenames that are thumbnail images
    LOOKS_LIKE_THUMBNAIL = re.compile('.+{0}'.format(THUMBNAIL_SUFFIX))

    # Format for serializing datetime objects.
    # Conforms to http://www.ietf.org/rfc/rfc3339.txt
    DT_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    @classmethod
    def _format_datetime(cls, v):
        """Returns string representation of v
        """
        return v.strftime(cls.DT_FORMAT)

    @classmethod
    def _parse_datetime(cls, v):
        """Returns datetime of v
        """
        return datetime.strptime(v, cls.DT_FORMAT).replace(tzinfo=pytz.timezone("UTC"))

    # TODO LH __eq__, __ne__?
    # TODO LH Store Rect instances within items
    # TODO LH Validate rotation?

    def __init__(self, scanned=None, scanned_path=None, thumbnail=None,
                 items=[], properties={}):
        """Scanned - InselectImage or None
        scanned_path - Path or None
        thumbnail - InselectImage or None
        items - list of dicts
        properties - dict
        """
        items = self._preprocess_items(items)

        # TODO Validate metadata fields
        # TODO Validate properties

        if scanned:
            # An InselectImage
            if not isinstance(scanned, InselectImage):
                raise InselectError('scanned should be an instance of InselectImage')
            else:
                self._scanned = scanned
        elif scanned_path:
            self._scanned = InselectImage(scanned_path)
        else:
            raise InselectError('Either scanned or scanned_path should be given')

        if thumbnail:
            if not isinstance(thumbnail, InselectImage):
                raise InselectError('thumbnail should be an instance of InselectImage')
            else:
                self._thumbnail = thumbnail
        else:
            self._thumbnail = InselectImage(
                self.thumbnail_path_of_scanned(self._scanned.path)
            )

        # Need either thumbnail or scanned
        if self._scanned.available or self._thumbnail.available:
            self._items = items
            self._properties = properties
        else:
            raise InselectError('Either scanned and/or thumbnail should be given')

    @classmethod
    def thumbnail_path_of_scanned(cls, scanned):
        """Returns the path of the thumbnail image for the given scanned image
        """
        scanned = Path(scanned)
        return scanned.parent / u'{0}{1}'.format(scanned.stem, cls.THUMBNAIL_SUFFIX)

    @classmethod
    def path_is_thumbnail_file(cls, path):
        """Returns True if path is a thumbnail file for an existing
        InselectDocument
        """
        doc = path.parent / path.name.replace(cls.THUMBNAIL_SUFFIX, cls.EXTENSION)
        return cls.LOOKS_LIKE_THUMBNAIL.match(str(path)) and doc.is_file()

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

    @property
    def properties(self):
        return self._properties

    def set_items(self, items):
        "Replace self.items with a deep copy of items"
        items = deepcopy(items)
        items = self._preprocess_items(items)
        self._items = items

    def _preprocess_items(self, items):
        # Returns items with tuples of boxes replaced with Rect instances and
        # metadata items with no values removed
        for i in xrange(0, len(items)):
            l, t, w, h = items[i]['rect']
            items[i]['rect'] = Rect(l, t, w, h)

            fields = items[i].get('fields', {})
            fields = {k: v for k, v in fields.iteritems() if '' != v}
            items[i]['fields'] = fields
        return items

    @classmethod
    def new_from_scan(cls, scanned,
                      thumbnail_width_pixels=THUMBNAIL_DEFAULT_WIDTH):
        """Creates, saves and returns a new InselectDocument for the scanned
        image
        """
        # TODO LH Raise error if a thumbnail image is ingested
        scanned = Path(scanned)
        if not scanned.is_file():
            raise InselectError(u'Image file [{0}] does not exist'.format(scanned))
        elif cls.path_is_thumbnail_file(scanned):
            msg = u'Cannot create a document for thumbnail file [{0}]'
            raise InselectError(msg.format(scanned))
        elif not cls.THUMBNAIL_MIN_WIDTH <= thumbnail_width_pixels <= cls.THUMBNAIL_MAX_WIDTH:
            raise InselectError('width should be between [{0}] and [{1}]'.format(
                cls.THUMBNAIL_MIN_WIDTH, cls.THUMBNAIL_MAX_WIDTH
            ))
        else:
            debug_print('Creating on image [{0}]'.format(scanned))
            doc = cls(scanned_path=scanned, items=[],
                      properties={'Created by': user_name(),
                                  'Created on': datetime.now(pytz.timezone("UTC")),
                                  })

            if doc.document_path.is_file():
                msg = u'Document file [{0}] already exists'
                raise InselectError(msg.format(doc.document_path))
            else:
                doc._create_and_load_thumbnail(thumbnail_width_pixels)
                doc.save()
                return doc

    @classmethod
    def load(cls, path):
        "Returns a new InselectDocument"
        debug_print('Loading from [{0}]'.format(path))

        path = Path(path)

        # Sniff the first few bytes - file must look like a json document
        if not re.match('^{[ (\n)|(\r\n)]*"', path.open('rb').read(20)):
            raise InselectError('Not an inselect document')
        else:
            doc = json.load(path.open(encoding='utf8'))
            v = doc.get('inselect version')

            if not v:
                raise InselectError('Not an inselect document')
            elif v not in cls.FILE_VERSIONS:
                raise InselectError('Unsupported version [{0}]'.format(v))
            else:
                if 1 == v:
                    # Version 1 contained just three illustrative fields -
                    # convert these to Darwin Core fields
                    for item in doc['items']:
                        fields = item['fields']
                        if fields.get('Taxonomic group'):
                            fields['scientificName'] = fields.pop('Taxonomic group')
                        if fields.get('Location'):
                            fields['otherCatalogNumbers'] = fields.pop('Location')
                        if fields.get('Specimen number'):
                            fields['catalogNumber'] = fields.pop('Specimen number')
                        item['fields'] = fields

                scanned = path.with_suffix(doc['scanned extension'])

                properties = doc.get('properties', {})

                # Parse datetimes
                for dt in {'Saved on', 'Created on'}.intersection(properties.keys()):
                    properties[dt] = cls._parse_datetime(properties[dt])

                msg = u'Loaded [{0}] items from [{1}]'
                debug_print(msg.format(len(doc['items']), path))

                return cls(scanned_path=scanned, items=doc['items'],
                           properties=properties)

    def save(self):
        "Saves to self.document_path"
        path = self.document_path
        debug_print(u'Saving [{0}] items to [{1}]'.format(len(self._items), path))

        # Convert Rect instances to lists
        items = deepcopy(self._items)
        for i in xrange(0, len(items)):
            items[i]['rect'] = tuple(items[i]['rect'])

        self.properties.update({'Saved by': user_name(),
                                'Saved on': datetime.now(pytz.timezone("UTC"))})

        properties = deepcopy(self.properties)

        # Format datetimes
        for dt in {'Saved on', 'Created on'}.intersection(properties.keys()):
            properties[dt] = self._format_datetime(properties[dt])

        doc = {
            'inselect version': self.FILE_VERSIONS[-1],
            'scanned extension': self._scanned.path.suffix,
            'items': items,
            'properties': properties,
        }

        # Tips from SO about reading and writing utf-8 encoded files with sorted
        # keys
        # http://stackoverflow.com/a/18337754/1773758
        # http://stackoverflow.com/a/20776329/1773758
        # Specify separators to prevent trailing whitespace
        with path.open("w", newline='\n', encoding='utf8') as f:
            f.write(unicode(json.dumps(doc, ensure_ascii=False, indent=4,
                                       separators=(',', ': '), sort_keys=True)))

        debug_print(u'Saved [{0}] items to [{1}]'.format(len(items), path))

    @property
    def crops(self):
        "Iterate over cropped object image arrays"
        return self._scanned.crops((i['rect'] for i in self._items),
                                   (i.get('rotation', 0) for i in self._items))

    def save_crops_from_image(self, image, crop_paths, progress=None):
        "Saves images cropped from image to dir. dir must exist."
        boxes = (i['rect'] for i in self._items)
        rotation = (i.get('rotation', 0) for i in self._items)
        image.save_crops(boxes, crop_paths, rotation, progress)

    def _create_and_load_thumbnail(self, width):
        "Create thumbnail image"
        # TODO LH Delegate job of creating thumbnail to InselectImage class
        import cv2

        p = self.thumbnail_path_of_scanned(self._scanned.path)

        msg = u'Creating [{0}] with width of [{1}] pixels'
        debug_print(msg.format(p, width))

        img = self._scanned.array
        factor = float(width) / img.shape[1]
        debug_print('Resizing to [{0}] pixels wide'.format(width))
        thumbnail = cv2.resize(img, (0, 0), fx=factor, fy=factor)
        debug_print('Writing to [{0}]'.format(p))
        # TODO Copy EXIF tags?
        res = cv2.imwrite(str(p), thumbnail)
        if not res:
            msg = u'Unable to write thumbnail [{0}]'
            raise InselectError(msg.format(p))

        # Load it
        self._thumbnail = InselectImage(p)

    @property
    def metadata_fields(self):
        """An iterable of metadata field names
        """
        # The union of fields among all items
        return set(chain(*(i['fields'].keys() for i in self._items)))
