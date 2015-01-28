
from .document import InselectDocument
from .inselect_error import InselectError
from .utils import debug_print, make_readonly

IMAGE_SUFFIXES = ('.tiff', '.png', '.jpeg', '.jpg')
IMAGE_PATTERNS = tuple(['*{0}'.format(s) for s in IMAGE_SUFFIXES])

def ingest_image(source, dest_dir):
    """Copies the image in the path source to the directory in the path
    dest_dir. Creates an returns a new instance of InselectDocument for the
    copied image.
    """
    dest = dest_dir / source.name
    if source!=dest and dest.is_file():
        raise InselectError('Destination image [{0}] exists'.format(dest))
    else:
        debug_print('Ingesting [{0}] to [{1}]'.format(source, dest))

        if source!=dest:
            source.rename(dest)

        # Raises if the document already exists
        doc = InselectDocument.new_from_scan(dest)

        doc.ensure_thumbnail()

        # Make images read-only
        debug_print('Making image files read-only')
        make_readonly(doc.scanned.path)
        make_readonly(doc.thumbnail.path)

        # TODO LH Copy EXIF tags?
        debug_print('Ingested [{0}] to [{1}]'.format(source, dest))

        return doc
