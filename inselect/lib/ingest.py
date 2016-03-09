import re

from .document import InselectDocument
from .inselect_error import InselectError
from .utils import debug_print, make_readonly

# Supported image formats
IMAGE_SUFFIXES = ('.bmp', '.jpeg', '.jpg', '.png', '.tif', '.tiff',)

# A case-insensitive regular expression that matches each suffix
IMAGE_SUFFIXES_RE = '|'.join('{0}'.format(p[1:]) for p in IMAGE_SUFFIXES)
IMAGE_SUFFIXES_RE = '^.*\\.({0})$'.format(IMAGE_SUFFIXES_RE)
IMAGE_SUFFIXES_RE = re.compile(IMAGE_SUFFIXES_RE, re.IGNORECASE)

# Patterns in the form *.bmp, *.jpeg etc
IMAGE_PATTERNS = tuple(['*{0}'.format(s) for s in IMAGE_SUFFIXES])


def ingest_image(source, dest_dir,
                 thumbnail_width_pixels=InselectDocument.THUMBNAIL_DEFAULT_WIDTH,
                 default_metadata_items=None,
                 cookie_cutter=None):
    """Copies the image in the path source to the directory in the path
    dest_dir. Creates an returns a new instance of InselectDocument for the
    copied image.

    default_metadata_items should be either None or a list of dicts.
    cookie_cutter should be either None or an instance of lib.CookieCutter.

    Default metadata takes precedence - cookie cutter items are applied only if
    default_metadata_items is None.

    An exception is raised if the destination image exists.
    An exception is raised if the Inselect document already exists.
    """
    dest = dest_dir / source.name
    if source != dest and dest.is_file():
        raise InselectError('Destination image [{0}] exists'.format(dest))
    else:
        debug_print('Ingesting [{0}] to [{1}]'.format(source, dest))

        if source != dest:
            source.rename(dest)

        # Raises if the document already exists
        doc = InselectDocument.new_from_scan(dest)

        doc.ensure_thumbnail(thumbnail_width_pixels)

        if default_metadata_items:
            debug_print('Adding [{0}] default metadata items'.format(
                len(default_metadata_items)
            ))
            doc.set_items(default_metadata_items)
            doc.save()
        elif cookie_cutter:
            debug_print('Adding cookie cutter items')
            cookie_cutter.apply(doc)
            doc.save()

        # Make images read-only
        debug_print('Making image files read-only')
        make_readonly(doc.scanned.path)
        make_readonly(doc.thumbnail.path)

        # TODO LH Copy EXIF tags?
        debug_print('Ingested [{0}] to [{1}]'.format(source, dest))

        return doc
