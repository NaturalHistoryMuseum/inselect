import json
import shutil
import tempfile
import unittest

from itertools import izip
from pathlib import Path

import numpy as np

import cv2

from inselect.lib.document import InselectImage, InselectDocument
from inselect.lib.document import validate_normalised
from inselect.lib.inselect_error import InselectError
from inselect.lib.rect import Rect
from inselect.lib.utils import make_readonly


TESTDATA = Path(__file__).parent / 'test_data'


# TODO LH Test read-only attributes

class TestValidateNormalised(unittest.TestCase):
    def test_validate_normalised(self):
        validate_normalised([Rect(0,0,1,1)])
        self.assertRaises(InselectError, validate_normalised, [(-0.1, 0,    1,   1)])
        self.assertRaises(InselectError, validate_normalised, [( 0,  -0.1,  1,   1)])
        self.assertRaises(InselectError, validate_normalised, [( 0,   0,    1.1, 1)])
        self.assertRaises(InselectError, validate_normalised, [( 0,   0,    1,   1.1)])


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
             shutil.rmtree(temp)


class TestDocument(unittest.TestCase):
    def test_load(self):
        path = TESTDATA / 'test_segment.inselect'
        doc = InselectDocument.load(path)

        self.assertEqual(doc.document_path, path)
        with self.assertRaises(AttributeError):
            doc.document_path = ''

        self.assertEqual(5, len(doc.items))
        with self.assertRaises(AttributeError):
            doc.items = []

        self.assertEqual(doc.scanned.path, path.with_suffix('.png'))
        self.assertTrue(doc.thumbnail is None)

    def test_load_bad_document(self):
        f = tempfile.NamedTemporaryFile()
        json.dump({'x': 1}, f)
        f.seek(0)
        self.assertRaises(InselectError, InselectDocument.load, f.name)

    def test_load_bad_version(self):
        f = tempfile.NamedTemporaryFile()
        json.dump({'inselect version': 1000}, f)
        f.seek(0)
        self.assertRaises(InselectError, InselectDocument.load, f.name)

    def test_load_images(self):
        source = TESTDATA / 'test_segment.inselect'
        temp = tempfile.mkdtemp()
        try:
            doc_temp = Path(temp) / 'test_segment.inselect'
            doc_temp.open('w').write(source.open().read())

            # Document load with no scanned image file
            self.assertRaises(InselectError, InselectDocument.load, doc_temp)

            # Document load with scanned image file present
            scanned_temp = Path(temp) / 'test_segment.png'
            scanned_temp.open('w')       # File only needs to exist
            actual = InselectDocument.load(doc_temp)
            self.assertEqual(InselectDocument.load(source).items, actual.items)
            self.assertFalse(actual.thumbnail)

            # Document load with scanned and thumbnail files present
            thumbnail_temp = Path(temp) / 'test_segment_thumbnail.jpg'
            thumbnail_temp.open('w')       # File only needs to exist
            actual = InselectDocument.load(doc_temp)
            self.assertEqual(InselectDocument.load(source).items, actual.items)
            self.assertTrue(actual.thumbnail)
        finally:
             shutil.rmtree(temp)

    def test_save(self):
        source = TESTDATA / 'test_segment.inselect'
        temp = tempfile.mkdtemp()
        try:
            doc_temp = Path(temp) / 'test_segment.inselect'
            doc_temp.open('w').write(source.open().read())

            scanned_temp = Path(temp) / 'test_segment.png'
            scanned_temp.open('w')       # File only needs to exist

            items = [ {'rect': Rect(0.1, 0.2, 0.5, 0.5) }, ]

            d = InselectDocument.load(doc_temp)
            d.set_items(items)
            d.save()

            self.assertEqual(items, InselectDocument.load(doc_temp).items)
        finally:
             shutil.rmtree(temp)

    def test_repr(self):
        path = TESTDATA / 'test_segment.inselect'
        doc = InselectDocument.load(path)
        expected = "InselectDocument ['{0}'] [5 items]".format(str(doc.scanned.path))
        self.assertEqual(expected, repr(doc))

    def test_crops_dir(self):
        doc = InselectDocument.load(TESTDATA / 'test_segment.inselect')
        self.assertEqual(TESTDATA / 'test_segment_crops', doc.crops_dir)
        with self.assertRaises(AttributeError):
            doc.crops_dir = ''

    def test_crops(self):
        path = TESTDATA / 'test_segment.inselect'
        doc = InselectDocument.load(path)

        self.assertEqual(5, len(doc.items))
        boxes = doc.scanned.from_normalised([i['rect'] for i in doc.items])
        for box, crop in izip(boxes, doc.crops):
            x0, y0, x1, y1 = box.coordinates
            self.assertTrue(np.all(doc.scanned.array[y0:y1, x0:x1] ==
                                   crop))

    def test_save_crops(self):
        path = TESTDATA / 'test_segment.inselect'
        doc = InselectDocument.load(path)

        crops_dir = doc.save_crops()
        try:
            self.assertTrue(crops_dir.is_dir())
            self.assertEqual(crops_dir, doc.crops_dir)
            self.assertEqual(5, len(list(crops_dir.glob('*.png'))))

            boxes = doc.scanned.from_normalised([i['rect'] for i in doc.items])
            for box, path in izip(boxes, sorted(crops_dir.glob('*.png'))):
                x0, y0, x1, y1 = box.coordinates
                self.assertTrue(np.all(doc.scanned.array[y0:y1, x0:x1] ==
                                       cv2.imread(str(path))))
        finally:
             shutil.rmtree(str(crops_dir))

    def test_set_items(self):
        path = TESTDATA / 'test_segment.inselect'
        doc = InselectDocument.load(path)

        items = [ {'rect': Rect(0, 0, 0.5, 0.5)}, ]
        doc.set_items(items)
        self.assertEqual(items, doc.items)

        # Not normalised
        items = [ {'rect': Rect(0, 0, 1, 2)}, ]
        self.assertRaises(InselectError, doc.set_items, items)

    def test_new_from_scan(self):
        temp = tempfile.mkdtemp()
        try:
            temp = Path(temp)
            img = temp / 'test.jpg'
            img.open('w')       # File only needs to exist

            doc = InselectDocument.new_from_scan(img)
            self.assertTrue(doc.document_path.is_file())
            self.assertEqual(img, doc.scanned.path)
        finally:
             shutil.rmtree(str(temp))

    def test_new_from_scan_doc_exists(self):
        path = TESTDATA / 'test_segment.png'
        self.assertRaises(InselectError, InselectDocument.new_from_scan, path)

    def test_new_from_scan_no_image(self):
        # Image does not exist
        self.assertRaises(InselectError, InselectDocument.new_from_scan, 'i am not a file')

    def test_ensure_thumbnail(self):
        source_doc = TESTDATA / 'test_segment.inselect'
        source_img = TESTDATA / 'test_segment.png'
        temp = tempfile.mkdtemp()
        try:
            doc_temp = Path(temp) / 'test_segment.inselect'
            doc_temp.open('w').write(source_doc.open().read())

            scan_tmp = Path(temp) / 'test_segment.png'
            scan_tmp.open('wb').write(source_img.open('rb').read())

            # Document load with no scanned image file
            doc = InselectDocument.load(doc_temp)
            self.assertTrue(doc.thumbnail is None)
            doc.ensure_thumbnail(width=2048)
            self.assertEqual(2048, doc.thumbnail.array.shape[1])
        finally:
             shutil.rmtree(str(temp))

    def test_ensure_thumbnail_failures(self):
        source_doc = TESTDATA / 'test_segment.inselect'
        source_img = TESTDATA / 'test_segment.png'
        temp = tempfile.mkdtemp()
        try:
            doc_temp = Path(temp) / 'test_segment.inselect'
            doc_temp.open('w').write(source_doc.open().read())

            scan_tmp = Path(temp) / 'test_segment.png'
            scan_tmp.open('wb').write(source_img.open('rb').read())

            doc = InselectDocument.load(doc_temp)

            self.assertRaises(InselectError, doc.ensure_thumbnail, 50)
            self.assertRaises(InselectError, doc.ensure_thumbnail, 20000)

            # TODO LH Assert that failure to create thumbnail raises
        finally:
            shutil.rmtree(str(temp))


if __name__=='__main__':
    unittest.main()
