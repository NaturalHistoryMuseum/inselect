import json
import shutil
import tempfile
import unittest

from itertools import izip
from pathlib import Path

import numpy as np

import cv2

from inselect.lib.document import InselectDocument
from inselect.lib.inselect_error import InselectError
from inselect.lib.rect import Rect


TESTDATA = Path(__file__).parent / 'test_data'

# TODO LH Test read-only attributes

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
