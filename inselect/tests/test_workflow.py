import cv2

import tempfile
import shutil
import tempfile
import unittest

from pathlib import Path

import numpy as np

from inselect.lib.document import InselectDocument
from inselect.lib.inselect_error import InselectError
from inselect.workflow.ingest import ingest, ingest_image
from inselect.workflow.segment import segment


TESTDATA = Path(__file__).parent / 'test_data'


class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.inbox = tempfile.mkdtemp()
        self.docs = tempfile.mkdtemp()

    def tearDown(self):
        try:
            shutil.rmtree(self.inbox)
        finally:
            shutil.rmtree(self.docs)

class TestIngest(TestWorkflow):
    def test_ingest_fail(self):
        # Inbox does not exist
        self.assertRaises(InselectError, ingest, Path('I am not a directory'),
                          Path(self.docs))

    def test_ingest_create_docs(self):
        # Document dir should be created
        docs = Path(self.docs) / 'I do not yet exist'
        self.assertFalse(docs.is_dir())

        img = cv2.imread(str(TESTDATA / 'test_segment.png'))

        inbox_img = Path(self.inbox) / 'x.tiff'

        cv2.imwrite(str(inbox_img), img)
        ingest(self.inbox, docs)

        self.assertTrue(docs.is_dir())

    def test_ingest(self):
        # Ingest from tiff
        inbox_img = Path(self.inbox) / 'x.tiff'
        docs_img = Path(self.docs) / 'x.tiff'

        img = cv2.imread(str(TESTDATA / 'test_segment.png'))
        cv2.imwrite(str(inbox_img), img)

        ingest(self.inbox, self.docs)

        # Document, scan and thumbnail should all exists
        self.assertTrue((Path(self.docs) / 'x.inselect').is_file())
        self.assertTrue(docs_img.is_file())
        self.assertTrue((Path(self.docs) / 'x_thumbnail.jpg').is_file())

        # Scan should have been removed from inbox
        self.assertFalse(inbox_img.is_file())

        # Scan is as expected?
        doc = InselectDocument.load(Path(self.docs) / 'x.inselect')
        self.assertTrue(np.all(img==doc.scanned.array))
        self.assertTrue(doc.thumbnail.array.shape[1], 4096)

        # TODO LH Assert images are read-only

        # Call ingest_image() because ingest() swallows errors
        cv2.imwrite(str(inbox_img), img)
        self.assertRaises(InselectError, ingest_image, inbox_img, Path(self.docs))


class TestSegment(TestWorkflow):
    def test_segment(self):
        # Ingest from tiff
        img = cv2.imread(str(TESTDATA / 'test_segment.png'))
        cv2.imwrite(str(Path(self.inbox) / 'x.tiff'), img)

        ingest(self.inbox, self.docs)

        doc = InselectDocument.load(Path(self.docs) / 'x.inselect')
        self.assertEqual(0, len(doc.items))

        segment(self.docs)

        doc = InselectDocument.load(Path(self.docs) / 'x.inselect')
        self.assertEqual(5, len(doc.items))

        # TODO LH assert that segment again does not touch this document


# TODO LH test read barcodes


if __name__=='__main__':
    unittest.main()
