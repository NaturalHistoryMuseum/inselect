import errno
import shutil

from collections import defaultdict
from functools import partial
from itertools import count
from pathlib import Path

import unicodecsv

from .validate_document import validate_document
from .utils import debug_print


class DocumentExport(object):
    def __init__(self, metadata_template):
        if not metadata_template:
            raise ValueError('Missing metadata_template')
        else:
            self._template = metadata_template

    def crop_fnames(self, document):
        """Generator function of instances of string. Where filenames collide,
        a suffix is appended, starting with '-1'
        """
        fnames = (
            self._template.format_label(1 + index, box['fields'])
            for index, box in enumerate(document.items)
        )

        # Set of fnames that have been yielded
        seen = set()
        # Mapping from base_fname to iterator of integer suffixes
        suffix = defaultdict(partial(count, start=1))
        for base_fname in fnames:
            fname = base_fname
            while fname in seen:
                fname = u'{0}-{1}'.format(base_fname, next(suffix[base_fname]))
            seen.add(fname)
            yield u'{0}{1}'.format(fname, self._template.cropped_file_suffix)

    def crops_dir(self, document):
        return document.crops_dir

    def save_crops(self, document, progress=None):
        """Saves images cropped from document.scanned to document.crops_dir.
        If document.crops_dir already exists, it is unlinked first.
        """
        if progress:
            progress('Removing existing saved crops')

        crops_dir = self.crops_dir(document)
        try:
            shutil.rmtree(unicode(crops_dir))
        except OSError as e:
            if errno.ENOENT == e.errno:
                # Directory does not exist - do nothing
                pass
            else:
                # Some other error
                raise

        crop_fnames = self.crop_fnames(document)
        crops_dir.mkdir()
        document.save_crops_from_image(
            document.scanned,
            (crops_dir / fn for fn in crop_fnames),
            progress
        )
        return crops_dir

    def csv_path(self, document):
        return document.document_path.with_suffix('.csv')

    def export_csv(self, document, path=None):
        """Exports metadata to a CSV file given in path, defaults to
        document.document_path with .csv extension. Path is returned.
        """
        if not path:
            path = self.csv_path(document)
        else:
            path = Path(path)

        debug_print(u'DocumentExport.export_csv to [{0}]'.format(path))

        # Field names
        fields = list(self._template.field_names())

        # Append fields that are in the document and not the template
        fields += sorted(f for f in document.metadata_fields if f not in fields)

        # Crop filenames
        crop_fnames = self.crop_fnames(document)

        with path.open('wb') as f:
            w = unicodecsv.writer(f, encoding='utf8')
            w.writerow(fields)
            for exported in self._template.export_items(crop_fnames, document):
                # Write metadata values in the correct order
                w.writerow(exported.get(f) for f in fields)

        return path

    def validation_problems(self, document):
        """Validates the document against the user template and returns any
        validation problems
        """
        return validate_document(document, self._template)
