import unittest
import shutil
import tempfile

from pathlib import Path

import cv2

import numpy as np

from inselect.lib.document import InselectDocument
from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import rmtree_readonly
from inselect.workflow.ingest import ingest_from_directory


TESTDATA = Path(__file__).parent.parent / 'test_data'


# TODO LH Many more tests required

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


if __name__=='__main__':
    unittest.main()
