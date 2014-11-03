import cv2

import tempfile
import shutil
import tempfile
import unittest

from pathlib import Path

import numpy as np

from inselect.lib.document import InselectDocument
from inselect.lib.inselect_error import InselectError
from inselect.workflow.ingest import ingest
from inselect.workflow.segment import segment_pending
from inselect.workflow.post_process import post_process


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

    def test_ingest(self):
        # Ingest from tiff
        img = cv2.imread(str(TESTDATA / 'test_segment.png'))
        cv2.imwrite(str(Path(self.inbox) / 'x.tiff'), img)

        ingest(self.inbox, self.docs)

        # Document, scan and thumbnail should all exists
        doc = InselectDocument.load(Path(self.docs) / 'x.inselect')

        # Scan is as expected?
        self.assertTrue(np.all(img==doc.scanned.array))

        self.assertTrue(doc.thumbnail.array.shape[1], 4096)

        # TODO LH Assert images are read-only
        # TODO LH Assert import of inbox/x.tiff should fail because
        #         it exists in docs

    def test_segment(self):
        # Ingest from tiff
        img = cv2.imread(str(TESTDATA / 'test_segment.png'))
        cv2.imwrite(str(Path(self.inbox) / 'x.tiff'), img)

        ingest(self.inbox, self.docs)

        doc = InselectDocument.load(Path(self.docs) / 'x.inselect')
        self.assertEqual(0, len(doc.items))

        segment_pending(self.docs)

        doc = InselectDocument.load(Path(self.docs) / 'x.inselect')
        self.assertEqual(5, len(doc.items))

    # TODO LH test post_process


if __name__=='__main__':
    unittest.main()
