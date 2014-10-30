import traceback


from pathlib import Path


from inselect.lib.document import InselectDocument
from inselect.lib.segment import segment_edges
from inselect.lib.utils import debug_print
from inselect.lib.rect import Rect


import inselect.lib.utils
inselect.lib.utils.DEBUG_PRINT = True


def segment_pending(dir):
    dir = Path(dir)
    for p in dir.glob('*.inselect'):
        doc = InselectDocument.load(p)
        if not doc.items:
            try:
                print('Will segment [{0}]'.format(p))

                # TODO LH This logic belongs in a Segmenter class
                if doc.thumbnail:
                    debug_print('Will segment on thumbnail')
                    img = doc.thumbnail
                else:
                    debug_print('Will segment on scan')
                    img = doc.scanned

                debug_print('Segmenting [{0}]'.format(p))
                rects,junk = segment_edges(img.array,
                                           variance_threshold=100,
                                           size_filter=1)
                rects = map(lambda r: Rect(r[0], r[1], r[2], r[3]), rects)
                rects = img.to_normalised(rects)
                items = [{"fields": {}, 'rect': r} for r in rects]
                doc.set_items(items)
                doc.save()
            except Exception:
                print('Error segmenting [{0}]'.format(p))
                traceback.print_exc()
        else:
            print('Skipping [{0}] as it already contains items'.format(p))


if __name__=='__main__':
    import config
    segment_pending(config.inselect)
