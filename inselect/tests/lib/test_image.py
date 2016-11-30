import shutil
import sys
import tempfile
import unittest

from itertools import repeat
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
        p = TESTDATA / 'shapes.png'
        i = InselectImage(p)
        self.assertEqual(p, i.path)

        # Check read-only
        with self.assertRaises(AttributeError):
            i.path = ''

        self.assertTrue(i.available)
        self.assertTrue(i.assert_is_file)

    def test_non_existent_file(self):
        img = InselectImage(TESTDATA / 'i am not a file.png')
        self.assertFalse(img.available)
        self.assertRaises(InselectError, img.assert_is_file)

    def test_not_an_image(self):
        f = tempfile.NamedTemporaryFile()
        i = InselectImage(f.name)
        self.assertTrue(i.available)
        self.assertTrue(i.assert_is_file)
        with self.assertRaises(InselectError):
            i.array

    def test_repr(self):
        p = TESTDATA / 'shapes.png'
        i = InselectImage(p)
        self.assertEqual("InselectImage('{0}')".format(str(p)), repr(i))

    def test_str(self):
        p = TESTDATA / 'shapes.png'
        i = InselectImage(p)
        self.assertEqual("InselectImage ['{0}'] [Unloaded]".format(str(p)), str(i))
        i.array    # Forces image to be read
        self.assertEqual("InselectImage ['{0}'] [Loaded]".format(str(p)), str(i))

    def test_array(self):
        "Array is read-only and has the expected dimensions"
        i = InselectImage(TESTDATA / 'shapes.png')
        self.assertFalse(i._array)
        self.assertEqual((437, 459), i.array.shape[:2])
        with self.assertRaises(AttributeError):
            i.array = ''

    def test_from_normalised(self):
        "Crops from normalised coordinates are as expected"
        i = InselectImage(TESTDATA / 'shapes.png')
        h, w = i.array.shape[:2]
        boxes = [Rect(0, 0, 1, 1), Rect(0, 0.2, 0.1, 0.8)]
        self.assertEqual([Rect(0, 0, 459, 437), Rect(0, 87, 46, 350)],
                         list(i.from_normalised(boxes)))

    def test_to_normalised(self):
        i = InselectImage(TESTDATA / 'shapes.png')
        boxes = [Rect(0, 0, 459, 437), Rect(0, 0, 153, 23)]
        self.assertEqual([Rect(0, 0, 1, 1), Rect(0, 0, 1.0/3, 1.0/19)],
                         list(i.to_normalised(boxes)))

    def test_overwrite_existing_crop(self):
        "Overwrite an existing file with a crop that is the entire image"
        i = InselectImage(TESTDATA / 'shapes.png')
        temp = tempfile.mkdtemp()
        try:
            p = Path(temp) / 'whole.png'

            # Create an image that is all black
            self.assertTrue(cv2.imwrite(str(p),
                            np.zeros((500, 500, 3), dtype='uint8')))

            # A crop that is the entire image
            i.save_crops([Rect(0, 0, 1, 1)], [p])

            crop = InselectImage(p).array

            # Crop should be the same shape as the image
            self.assertEqual(i.array.shape, crop.shape)

            # Crop should have the same pixels as the image
            self.assertTrue(np.all(i.array == crop))
        finally:
            shutil.rmtree(temp)

    def test_save_crop_partial(self):
        "Save a crop that is a portion of the image"
        i = InselectImage(TESTDATA / 'shapes.png')
        temp = tempfile.mkdtemp()
        try:
            # A crop that is a portion of the image
            p = Path(temp) / 'partial.png'
            i.save_crops([Rect(0.1, 0.2, 0.4, 0.3)], [p])

            crop = InselectImage(p).array

            # Crop should have this shape
            self.assertEqual((131, 184, 3), crop.shape)

            # Crop should have these pixels
            expected = i.array[87:218, 46:230]
            self.assertTrue(np.all(expected == InselectImage(p).array))
        finally:
            shutil.rmtree(temp)

    def test_save_crop_overlapping(self):
        "Save a crop that is partially overlapping the image"
        i = InselectImage(TESTDATA / 'shapes.png')
        temp = tempfile.mkdtemp()
        try:
            # A crop that is partially overlapping the image
            p = Path(temp) / 'overlapping.png'

            i.save_crops([Rect(-0.1, -0.1, 0.4, 0.3)], [p])

            crop = InselectImage(p).array

            # Crop should have this shape
            self.assertEqual((131, 184, 3), crop.shape)

            # Non-intersecting regions should be all zeroes
            self.assertTrue(np.all(0 == crop[0:44, 0:46]))
            self.assertTrue(np.all(0 == crop[0:44, ]))
            self.assertTrue(np.all(0 == crop[:, 0:46]))
            coords = list(i.from_normalised([Rect(-0.1, -0.1, 0.4, 0.3)]))

            expected = i.array[0:87, 0:138, ]

            self.assertTrue(np.all(expected == crop[44:, 46:, ]))
        finally:
            shutil.rmtree(temp)

    def test_save_crop_outside(self):
        "Save a crop that is a entirely outside of the image"
        i = InselectImage(TESTDATA / 'shapes.png')
        temp = tempfile.mkdtemp()
        try:
            # A crop that is a entirely outside of the image
            p = Path(temp) / 'outside.png'
            i.save_crops([Rect(-1.5, -5.0, 1.0, 3.0)], [p])

            crop = InselectImage(p).array

            # Crop should have this shape
            self.assertEqual((1311, 459, 3), crop.shape)

            # All of the crop should be all zeroes
            self.assertTrue(np.all(0 == crop))
        finally:
            shutil.rmtree(temp)

    def test_save_crops_progress(self):
        "Check values passed to callable of save_crops"
        i = InselectImage(TESTDATA / 'shapes.png')
        temp = tempfile.mkdtemp()
        try:
            progress = Mock(return_value=None)
            i.save_crops([Rect(0, 0, 1, 1)],
                         [Path(temp) / 'whole.png'],
                         progress=progress)
            progress.assert_called_once_with('Writing crop 1')
        finally:
            shutil.rmtree(temp)

    def test_save_crops_all_rotated90(self):
        "All crops are saved with 90 degrees of clockwise rotation"
        i = InselectImage(TESTDATA / 'shapes.png')
        temp = tempfile.mkdtemp()
        try:
            i.save_crops(repeat(Rect(0, 0, 1, 1), 4),
                         (Path(temp) / '{0}.png'.format(n) for n in xrange(0, 4)),
                         rotation=90)
            crop = cv2.imread(str(Path(temp) / '0.png'))
            self.assertTrue(np.all(cv2.flip(cv2.transpose(i.array), 1) == crop))
            crop = cv2.imread(str(Path(temp) / '1.png'))
            self.assertTrue(np.all(cv2.flip(cv2.transpose(i.array), 1) == crop))
            crop = cv2.imread(str(Path(temp) / '2.png'))
            self.assertTrue(np.all(cv2.flip(cv2.transpose(i.array), 1) == crop))
            crop = cv2.imread(str(Path(temp) / '3.png'))
            self.assertTrue(np.all(cv2.flip(cv2.transpose(i.array), 1) == crop))
        finally:
            shutil.rmtree(temp)

    def test_save_crops_all_rotated(self):
        "Crops are saved with different rotations"
        i = InselectImage(TESTDATA / 'shapes.png')
        temp = tempfile.mkdtemp()
        try:
            i.save_crops(repeat(Rect(0, 0, 1, 1), 4),
                         (Path(temp) / '{0}.png'.format(n) for n in xrange(0, 4)),
                         rotation=[0, 90, 180, -90])
            crop = cv2.imread(str(Path(temp) / '0.png'))
            self.assertTrue(np.all(i.array == crop))
            crop = cv2.imread(str(Path(temp) / '1.png'))
            self.assertTrue(np.all(cv2.flip(cv2.transpose(i.array), 1) == crop))
            crop = cv2.imread(str(Path(temp) / '2.png'))
            self.assertTrue(np.all(cv2.flip(i.array, -1) == crop))
            crop = cv2.imread(str(Path(temp) / '3.png'))
            self.assertTrue(np.all(cv2.flip(cv2.transpose(i.array), 0) == crop))
        finally:
            shutil.rmtree(temp)

    def test_crops_bad_rotation(self):
        "Generate crops with an illegal rotation"
        i = InselectImage(TESTDATA / 'shapes.png')
        # Need to use context manager because i.crops is a generator function
        with self.assertRaises(ValueError):
            list(i.crops([Rect(0, 0, 1, 1)], -1))

    @unittest.skipIf(sys.platform.startswith("win"),
                     "Read-only directories not available on Windows")
    def test_save_crops_read_only_directory(self):
        "Can't write crops to a read-only directory"
        # This case is doing more than simply testing filesystem behavour
        # because it tests the failure code in InselectImage
        temp = tempfile.mkdtemp()
        try:
            make_readonly(temp)

            i = InselectImage(TESTDATA / 'shapes.png')
            with self.assertRaises(InselectError):
                i.save_crops([Rect(0, 0, 1, 1)], [Path(temp) / 'x.png'])
        finally:
            rmtree_readonly(temp)

    def test_size_bytes(self):
        i = InselectImage(TESTDATA / 'shapes.png')
        self.assertEqual(18153, i.size_bytes)

        # Load the array and check again - different code path
        i.array
        self.assertEqual(18153, i.size_bytes)

    def test_dimensions(self):
        i = InselectImage(TESTDATA / 'shapes.png')
        self.assertEqual((459, 437), i.dimensions)

if __name__ == '__main__':
    unittest.main()
