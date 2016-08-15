import shutil
import tempfile

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
                fname = '{0}-{1}'.format(base_fname, next(suffix[base_fname]))
            seen.add(fname)
            yield '{0}{1}'.format(fname, self._template.cropped_file_suffix)

    def crops_dir(self, document):
        return document.crops_dir

    def save_crops(self, document, progress=None):
        """Saves images cropped from document.scanned to document.crops_dir.
        Crops are first written to a tempdir in the same directory as document.
        If it exists, document.crops_dir is unlinked, and the tempdir is
        renamed to document.crops_dir. Any existing data in document.crops_dir
        is therefore lost.
        """
        # Create temp dir alongside scan
        tempdir = tempfile.mkdtemp(
            dir=str(document.scanned.path.parent),
            prefix=document.scanned.path.stem + '_temp_crops'
        )
        tempdir = Path(tempdir)
        debug_print('Saving crops to to temp dir [{0}]'.format(tempdir))

        crop_fnames = self.crop_fnames(document)

        try:
            # Save crops
            document.save_crops_from_image(document.scanned,
                                           (tempdir / fn for fn in crop_fnames),
                                           progress)

            # rm existing crops dir
            crops_dir = self.crops_dir(document)
            shutil.rmtree(str(crops_dir), ignore_errors=True)

            # Rename temp dir
            debug_print('Moving temp crops dir [{0}] to [{1}]'.format(
                tempdir, crops_dir
            ))
            tempdir.rename(crops_dir)
            tempdir = None

            debug_print('Saved [{0}] crops to [{1}]'.format(
                document.n_items, crops_dir
            ))

            return crops_dir
        finally:
            if tempdir:
                shutil.rmtree(str(tempdir))

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

        debug_print('DocumentExport.export_csv to [{0}]'.format(path))

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
