import stat
import traceback

from pathlib import Path


from inselect.lib.document import InselectDocument, InselectImage
from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print, make_readonly


import inselect.lib.utils
inselect.lib.utils.DEBUG_PRINT = True


def ingest_image(source, dest):
    if source!=dest and dest.is_file():
        raise InselectError('Destination image [{0}] exists'.format(dest))
    else:
        debug_print('Ingesting [{0}] to [{1}]'.format(source, dest))
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

def ingest(inbox, docs):
    inbox, docs = Path(inbox), Path(docs)
    if not inbox.is_dir():
        raise InselectError('Inbox directory [{0}] does not exist'.format(inbox))

    if not docs.is_dir():
        print('Create document directory [{0}]'.format(docs))
        docs.mkdir(parents=True)

    for source in inbox.glob('*tiff'):
        try:
            dest = docs / source.name
            ingest_image(source, dest)
        except Exception:
            print('Error ingesting [{0}]'.format(source))
            traceback.print_exc()


if __name__=='__main__':
    import config
    ingest(config.inbox, config.inselect)
