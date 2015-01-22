import unittest
from pathlib import Path

from inselect.lib.document import InselectDocument
from inselect.lib.segment import segment_document


TESTDATA = Path(__file__).parent / 'test_data'


class TestSegment(unittest.TestCase):
    def test_segment_document(self):
        doc = InselectDocument.load(TESTDATA / 'test_segment.inselect')

        self.assertEqual(5, len(doc.items))

        # Compare the rects in pixels
        expected = doc.scanned.from_normalised([i['rect'] for i in doc.items])
        doc.set_items([])
        self.assertEqual(0, len(doc.items))

        doc, display_image = segment_document(doc)

        actual = doc.scanned.from_normalised([i['rect'] for i in doc.items])
        self.assertEqual(list(expected), list(actual))


if __name__=='__main__':
    unittest.main()
