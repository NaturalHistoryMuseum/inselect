import shutil
import sys
import tempfile
import unittest

from itertools import izip
from mock import Mock
from pathlib import Path

import numpy as np

import cv2

from inselect.lib.image import InselectImage
from inselect.lib.inselect_error import InselectError
from inselect.lib.rect import Rect
from inselect.lib.utils import make_readonly, rmtree_readonly

TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestImage(unittest.TestCase):
    def test_path(self):
        "Test path attribute"
        p = TESTDATA / 'test_segment.png'
        i = InselectImage(p)
        self.assertEqual(p, i.path)

        # Check read-only
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
        "Array is read-only and has the expected dimenions"
        i = InselectImage(TESTDATA / 'test_segment.png')
        self.assertFalse(i._array)
        self.assertEqual((437, 459), i.array.shape[:2])
        with self.assertRaises(AttributeError):
            i.array = ''

    def test_from_normalised(self):
        "Crops from normalised coordinates are as expected"
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

        # Check that valid boxes do not raise an error
        i.validate_in_bounds([(0,  0, 459, 437)])

        self.assertRaises(InselectError, i.validate_in_bounds, [(-1,  0, 459, 437)])
        self.assertRaises(InselectError, i.validate_in_bounds, [( 0, -1, 459, 437)])
        self.assertRaises(InselectError, i.validate_in_bounds, [( 0,  0, 460, 437)])
        self.assertRaises(InselectError, i.validate_in_bounds, [( 0,  0, 459, 438)])

    def test_save_crops(self):
        "Cropped images are as expected"
        i = InselectImage(TESTDATA / 'test_segment.png')
        temp = tempfile.mkdtemp()
        try:
            # A crop that is the entire image
            p = Path(temp) / 'whole.png'
            i.save_crops([Rect(0, 0, 1, 1)], [p])
            self.assertTrue(np.all(i.array==InselectImage(p).array))

            # A crop that is a portion of the image

            # Make sure that existing file is overwritten
            p = Path(temp) / 'partial.png'
            p.open('w')    # File just needs to exist
            i.save_crops([Rect(0.1, 0.2, 0.4, 0.3)], [p])
            expected = i.array[87:218, 45:228]
            self.assertTrue(np.all(expected==InselectImage(p).array))
        finally:
            shutil.rmtree(temp)

    def test_save_crops_progress(self):
        "Check values passed to callable of save_crops"
        i = InselectImage(TESTDATA / 'test_segment.png')
        temp = tempfile.mkdtemp()
        try:
            progress = Mock(return_value=None)
            i.save_crops([Rect(0, 0, 1, 1)],
                         [Path(temp) / 'whole.png'],
                         progress)
            progress.assert_called_once_with('Writing crop 1')
        finally:
            shutil.rmtree(temp)

    @unittest.skipIf(sys.platform.startswith("win"),
                     "Read-only directories not available on Windows")
    def test_save_crops_read_only_directory(self):
        "Can't write crops to a read-only directory"
        # This case is doing more than simply testing filesystem behavour
        # because it tests the failure code in InselectImage
        temp = tempfile.mkdtemp()
        try:
            make_readonly(temp)

            i = InselectImage(TESTDATA / 'test_segment.png')
            with self.assertRaises(InselectError):
                i.save_crops([Rect(0, 0, 1, 1)], [Path(temp) / 'x.png'])
        finally:
            rmtree_readonly(temp)


if __name__=='__main__':
    unittest.main()
