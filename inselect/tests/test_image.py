import shutil
import tempfile
import unittest

from itertools import izip
from pathlib import Path

import numpy as np

import cv2

from inselect.lib.image import InselectImage
from inselect.lib.inselect_error import InselectError
from inselect.lib.rect import Rect
from inselect.lib.utils import make_readonly, rmtree_readonly

TESTDATA = Path(__file__).parent / 'test_data'

# TODO LH Test read-only attributes

class TestImage(unittest.TestCase):
    def test_path(self):
        p = TESTDATA / 'test_segment.png'
        i = InselectImage(p)
        self.assertEqual(p, i.path)
        with self.assertRaises(AttributeError):
            i.path = ''

    def test_non_existent_file(self):
        self.assertRaises(InselectError, InselectImage, TESTDATA / 'i am not a file.png')

    def test_not_an_image(self):
        f = tempfile.NamedTemporaryFile()
        i = InselectImage(f.name)
        with self.assertRaises(InselectError):
            i.array

    def test_repr(self):
        p = TESTDATA / 'test_segment.png'
        i = InselectImage(p)
        self.assertEqual("InselectImage('{0}')".format(str(p)), repr(i))

    def test_str(self):
        p = TESTDATA / 'test_segment.png'
        i = InselectImage(p)
        self.assertEqual("InselectImage ['{0}'] [Unloaded]".format(str(p)), str(i))
        i.array    # Forces image to be read
        self.assertEqual("InselectImage ['{0}'] [Loaded]".format(str(p)), str(i))

    def test_array(self):
        i = InselectImage(TESTDATA / 'test_segment.png')
        self.assertFalse(i._array)
        self.assertEqual((437, 459), i.array.shape[:2])
        with self.assertRaises(AttributeError):
            i.array = ''

    def test_from_normalised(self):
        i = InselectImage(TESTDATA / 'test_segment.png')
        h,w = i.array.shape[:2]
        boxes = [Rect(0, 0, 1, 1), Rect(0, 0.2, 0.1, 0.8)]
        self.assertEqual([Rect(0, 0, 459, 437), Rect(0, 87, 45, 349)],
                         list(i.from_normalised(boxes)))

    def test_not_normalised(self):
        i = InselectImage(TESTDATA / 'test_segment.png')
        self.assertRaises(i.from_normalised([Rect(0, 0, 2, 2)]))

    def test_to_normalised(self):
        i = InselectImage(TESTDATA / 'test_segment.png')
        boxes = [Rect(0, 0, 459, 437), Rect(0, 0, 153, 23)]
        self.assertEqual([Rect(0, 0, 1, 1), Rect(0, 0, 1.0/3, 1.0/19)],
                         list(i.to_normalised(boxes)))

    def test_validate_in_bounds(self):
        i = InselectImage(TESTDATA / 'test_segment.png')
        self.assertRaises(InselectError, i.validate_in_bounds, [(-1,  0, 459, 437)])
        self.assertRaises(InselectError, i.validate_in_bounds, [( 0, -1, 459, 437)])
        self.assertRaises(InselectError, i.validate_in_bounds, [( 0,  0, 460, 437)])
        self.assertRaises(InselectError, i.validate_in_bounds, [( 0,  0, 459, 438)])

    def test_save_crops(self):
        temp = tempfile.mkdtemp()
        try:
            i = InselectImage(TESTDATA / 'test_segment.png')

            # Entire image
            p = Path(temp) / 'whole.png'
            i.save_crops([Rect(0, 0, 1, 1)], [p])
            self.assertTrue(np.all(i.array==InselectImage(p).array))

            # Subsection of image
            # Make sure that existing file is overwritten
            p = Path(temp) / 'partial.png'
            p.open('w')    # File just needs to exist
            i.save_crops([Rect(0.1, 0.2, 0.4, 0.3)], [p])
            expected = i.array[87:218, 45:228]
            self.assertTrue(np.all(expected==InselectImage(p).array))
        finally:
            shutil.rmtree(temp)

    def test_save_crops_read_only(self):
        # Try to save to existing read-only file
        temp = tempfile.mkdtemp()
        try:
            i = InselectImage(TESTDATA / 'test_segment.png')

            p = Path(temp) / 'readonly.png'
            p.open('w')    # File just needs to exist
            make_readonly(p)

            # Entire image
            with self.assertRaises(InselectError):
                i.save_crops([Rect(0, 0, 1, 1)], [p])
        finally:
            rmtree_readonly(temp)


if __name__=='__main__':
    unittest.main()
