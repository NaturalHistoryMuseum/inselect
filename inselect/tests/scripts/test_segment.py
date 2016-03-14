import unittest

from pathlib import Path

from inselect.lib.ingest import ingest_image
from inselect.lib.document import InselectDocument
from inselect.scripts.segment import main

from inselect.tests.utils import temp_directory_with_files


TESTDATA = Path(__file__).parent.parent / 'test_data'


# TODO LH Many more tests required

class TestSegment(unittest.TestCase):
    def test_segment(self):
        "Segment an existing document"

        with temp_directory_with_files(TESTDATA / 'test_segment.png') as tempdir:
            # Create a new document
            ingest_image(tempdir / 'test_segment.png', tempdir)

            main([unicode(tempdir)])

            doc_path = tempdir / 'test_segment.inselect'
            self.assertTrue(doc_path.is_file())
            doc = InselectDocument.load(doc_path)
            self.assertEqual(5, len(doc.items))

            # TODO LH assert that segment again does not touch this document


if __name__ == '__main__':
    unittest.main()
