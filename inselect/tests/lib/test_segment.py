import unittest
from pathlib import Path

from inselect.lib.document import InselectDocument
from inselect.lib.segment_document import SegmentDocument


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestSegment(unittest.TestCase):
    def _segment(self, doc, sort_by_columns, expected):
        self.assertEqual(5, len(doc.items))
        doc.set_items([])
        self.assertEqual(0, len(doc.items))

        segment_doc = SegmentDocument(sort_by_columns=sort_by_columns)
        doc, display_image = segment_doc.segment(doc)

        # Compare the rects in pixels
        actual = doc.scanned.from_normalised([i['rect'] for i in doc.items])
        self.assertEqual(list(expected), list(actual))

    def test_segment_document_sort_by_rows(self):
        "Segment the document with boxes sorted by rows"
        doc = InselectDocument.load(TESTDATA / 'shapes.inselect')
        expected = doc.scanned.from_normalised(
            [i['rect'] for i in doc.items]
        )
        self._segment(doc, False, expected)

    def test_segment_document_sort_by_columns(self):
        "Segment the document with boxes sorted by columns"
        doc = InselectDocument.load(TESTDATA / 'shapes.inselect')
        items = doc.items
        expected = doc.scanned.from_normalised(
            [items[index]['rect'] for index in (0, 3, 2, 1, 4)]
        )
        self._segment(doc, True, expected)


if __name__ == '__main__':
    unittest.main()
