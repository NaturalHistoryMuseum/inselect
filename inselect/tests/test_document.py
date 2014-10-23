import unittest
import shutil
import tempfile

from pathlib import Path

import numpy as np

from inselect.lib.document import InselectImage, InselectDocument
from inselect.lib.document import validate_normalised
from inselect.lib.inselect_error import InselectError
from inselect.lib.rect import Rect


TESTDATA = Path(__file__).parent / 'test_data'


class TestImage(unittest.TestCase):
    def test_open(self):
        i = InselectImage(TESTDATA / 'test_segment.png')
        self.assertFalse(i._npimage)

    def test_non_existent_file(self):
        self.assertRaises(InselectError, InselectImage, TESTDATA / 'i am not a file.png')

    def test_not_an_image(self):
        f = tempfile.NamedTemporaryFile()
        i = InselectImage(f.name)
        with self.assertRaises(InselectError):
            i.array

    def test_array(self):
        i = InselectImage(TESTDATA / 'test_segment.png')
        self.assertEqual((437, 459), i.array.shape[:2])

    def test_from_normalised(self):
        i = InselectImage(TESTDATA / 'test_segment.png')
        boxes = [Rect(0, 0, 1, 1), Rect(0, 0, 0.5, 0.5), ]
        self.assertEqual([Rect(0, 0, 459, 437), Rect(0, 0, 459/2, 437/2)],
                         list(i.from_normalised(boxes)))

    def test_not_normalised(self):
        i = InselectImage(TESTDATA / 'test_segment.png')
        self.assertRaises(i.from_normalised([Rect(0, 0, 2, 2)]))

    def test_to_normalised(self):
        i = InselectImage(TESTDATA / 'test_segment.png')
        boxes = [Rect(0, 0, 459, 437), Rect(0, 0, 153, 23)]
        self.assertEqual([Rect(0, 0, 1, 1), Rect(0, 0, 1.0/3, 1.0/19)],
                         list(i.to_normalised(boxes)))

    def test_out_of_bounds(self):
        i = InselectImage(TESTDATA / 'test_segment.png')
        self.assertRaises(i.to_normalised([Rect(0, 0, 460, 437)]))
        self.assertRaises(i.to_normalised([Rect(0, 0, 459, 438)]))

    def test_save_crops(self):
        dir = tempfile.mkdtemp()
        try:
            i = InselectImage(TESTDATA / 'test_segment.png')

            # Entire image
            p = Path(dir) / 'whole.png'
            i.save_crops([Rect(0, 0, 1, 1)], [p])
            self.assertTrue(np.all(i.array==InselectImage(p).array))

            # Subsection of image
            p = Path(dir) / 'partial.png'
            i.save_crops([Rect(0.1, 0.2, 0.5, 0.5)], [p])
            expected = i.array[87:392, 45:320]
            self.assertTrue(np.all(expected==InselectImage(p).array))
        finally:
             shutil.rmtree(dir)


if __name__=='__main__':
    unittest.main()
