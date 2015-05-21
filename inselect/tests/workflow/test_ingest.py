import unittest
import shutil
import tempfile

from pathlib import Path

import cv2

import numpy as np

from inselect.lib.document import InselectDocument
from inselect.lib.ingest import IMAGE_SUFFIXES_RE
from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import rmtree_readonly
from inselect.workflow.ingest import ingest_from_directory


TESTDATA = Path(__file__).parent.parent / 'test_data'


# TODO LH Many more tests required

class TestImagesSuffixesRe(unittest.TestCase):
    """Tests IMAGE_SUFFIXES_RE
    """
    def test_images_suffixes_re(self):
        re = IMAGE_SUFFIXES_RE
        self.assertRegexpMatches('x.jpg', re)
        self.assertRegexpMatches('x.Jpeg', re)
        self.assertRegexpMatches('x.TIFF', re)
        self.assertRegexpMatches('x.Tiff', re)

        self.assertNotRegexpMatches('x.jpgx', re)
        self.assertNotRegexpMatches('x.jpg ', re)
        self.assertNotRegexpMatches('x.txt', re)


class TestIngest(unittest.TestCase):
    def setUp(self):
        self.inbox = Path(tempfile.mkdtemp())
        self.docs = Path(tempfile.mkdtemp())

    def tearDown(self):
        try:
            rmtree_readonly(self.inbox)
        finally:
            rmtree_readonly(self.docs)

    def test_ingest_fail(self):
        "Inbox directory does not exist"
        self.assertRaises(InselectError, ingest_from_directory,
                          Path('I am not a directory'),
                          self.docs)

    def test_ingest_create_docs(self):
        "Document dir is created on ingest"
        docs = self.docs / 'I do not yet exist'
        self.assertFalse(docs.is_dir())

        # Create an image to ingest
        inbox_img = self.inbox / 'x.png'
        shutil.copy(str(TESTDATA / 'test_segment.png'), str(inbox_img))

        ingest_from_directory(self.inbox, docs)

        self.assertTrue(docs.is_dir())

    def test_ingest(self):
        "PNG image is ingested and document is created"
        inbox_img = self.inbox / 'x.png'
        docs_img = self.docs / 'x.png'

        shutil.copy(str(TESTDATA / 'test_segment.png'), str(inbox_img))

        # Read the image for comparison test
        original_image = cv2.imread(str(inbox_img))

        ingest_from_directory(self.inbox, self.docs)

        # Document, scan and thumbnail should all exists
        self.assertTrue((self.docs / 'x.inselect').is_file())
        self.assertTrue(docs_img.is_file())
        self.assertTrue((self.docs / 'x_thumbnail.jpg').is_file())

        # Scan should have been removed from inbox
        self.assertFalse(inbox_img.is_file())

        # Scan is as expected?
        doc = InselectDocument.load(self.docs / 'x.inselect')
        self.assertTrue(np.all(original_image == doc.scanned.array))
        self.assertTrue(doc.thumbnail.array.shape[1], 4096)

        # TODO LH Assert ingested images are read-only

    def test_extension_cases(self):
        "Ingestion of image files with extensions in various combinatons of case"
        # Create images to ingest
        lower = 'lower.png'
        upper = 'upper.png'
        title = 'title.Png'
        shutil.copy(str(TESTDATA / 'test_segment.png'), str(self.inbox / lower))
        shutil.copy(str(TESTDATA / 'test_segment.png'), str(self.inbox / upper))
        shutil.copy(str(TESTDATA / 'test_segment.png'), str(self.inbox / title))

        ingest_from_directory(self.inbox, self.docs)

        # Images should have been removed from inbox
        self.assertFalse((self.inbox / lower).is_file())
        self.assertFalse((self.inbox / upper).is_file())
        self.assertFalse((self.inbox / title).is_file())

        # Images should have been moved to docs dir
        self.assertTrue((self.docs / lower).is_file())
        self.assertTrue((self.docs / upper).is_file())
        self.assertTrue((self.docs / title).is_file())


if __name__=='__main__':
    unittest.main()
