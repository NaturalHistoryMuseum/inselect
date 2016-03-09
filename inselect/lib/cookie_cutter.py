"""Default bounding boxes
"""

import json

from copy import deepcopy
from itertools import chain
from pathlib import Path

from .inselect_error import InselectError


class CookieCutter(object):
    """Bounding boxes as a list of lists [x, y, width, height] of normalised
    (i.e., between 0 and 1) floats.
    """

    FILE_VERSIONS = (1,)
    EXTENSION = '.inselect_cookie_cutter'

    def __init__(self, name, boxes):
        if (not all(4 == len(box) for box in boxes) or
            not all(isinstance(v, float) for v in chain(*boxes))):
            raise ValueError('Must be a list of numeric coordinates')
        else:
            self._boxes = deepcopy(boxes)
            self.name = u'{0} ({1} boxes)'.format(
                name, len(self._boxes)
            )

    @classmethod
    def load(cls, path):
        """Returns a new instance of CookieCutter using the json document at
        path
        """
        with Path(path).open(encoding='utf8') as infile:
            doc = json.load(infile)

        version = doc.get('boxes version')

        if not version:
            raise InselectError('Not an inselect cookie cutter')
        elif version not in cls.FILE_VERSIONS:
            raise InselectError('Unsupported version [{0}]'.format(version))
        else:
            return cls(Path(path).stem, doc['boxes'])

    def save(self, path):
        """Writes boxes to path
        """
        doc = {
            'boxes version': self.FILE_VERSIONS[-1],
            'boxes': self._boxes,
        }
        with Path(path).open('w', encoding='utf8') as outfile:
            outfile.write(unicode(json.dumps(doc, indent=4)))

    @property
    def document_items(self):
        "Returns a list of dicts [{'rect': left, top, width, height}]"
        return [{'rect': v} for v in self._boxes]

    def apply(self, document):
        "Applies this cookie cutter to the document"
        document.set_items(self.document_items)
