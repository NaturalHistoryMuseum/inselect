import shutil
import tempfile

from itertools import chain, count, izip
from pathlib import Path

from .unicode_csv import UnicodeWriter
from .utils import debug_print


class DocumentExport(object):
    def __init__(self, metadata_template=None):
        self._template = metadata_template

    def crop_fnames(self, document):
        "Generator function of instances of string"
        if self._template:
            f = self._template.format_label
            fnames = (f(**i['fields']) for i in document.items)
        else:
            fnames = ('{0:04}'.format(1+i) for i in xrange(0, document.n_items))

        suffix = document.scanned.path.suffix
        return ('{0}{1}'.format(fn, suffix) for fn in fnames)

    def save_crops(self, document, progress=None):
        "Saves images cropped from document.scanned to document.crops_dir"
        # TODO LH Test that cancel of export leaves existing crops dir.
        # Create temp dir alongside scan
        tempdir = tempfile.mkdtemp(dir=str(document.scanned.path.parent),
            prefix=document.scanned.path.stem + '_temp_crops')
        tempdir = Path(tempdir)
        debug_print('Saving crops to to temp dir [{0}]'.format(tempdir))

        crop_fnames = self.crop_fnames(document)

        try:
            # Save crops
            document.save_crops_from_image(document.scanned,
                                           (tempdir / fn for fn in crop_fnames),
                                           progress)

            # rm existing crops dir
            crops_dir = document.crops_dir
            shutil.rmtree(str(crops_dir), ignore_errors=True)

            # Rename temp dir
            msg = 'Moving temp crops dir [{0}] to [{1}]'
            debug_print(msg.format(tempdir, crops_dir))
            tempdir.rename(crops_dir)
            tempdir = None

            msg = 'Saved [{0}] crops to [{1}]'
            debug_print(msg.format(document.n_items, crops_dir))

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

        debug_print(u'DocumentExport.export_csv to [{0}]'.format(path))

        # Field names
        if self._template:
            fields = [f['Name'] for f in self._template.fields]

            # Append fields that are in the document and not the template
            fields += [f for f in document.metadata_fields if f not in fields]
        else:
            fields = sorted(document.metadata_fields)

        crop_fnames = self.crop_fnames(document)

        with path.open('wb') as f:
            w = UnicodeWriter(f)
            w.writerow(chain(['Item','Cropped_image_name'], fields))
            for index, fname, item in izip(count(), crop_fnames, document.items):
                w.writerow(chain([1+index, fname],
                                 (item['fields'].get(f) for f in fields)))

        return path
