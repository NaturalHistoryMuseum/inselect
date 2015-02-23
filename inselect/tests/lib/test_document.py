import json
import os
import shutil
import stat
import tempfile
import unittest

from itertools import izip, count
from pathlib import Path

import numpy as np

import cv2

from inselect.lib.document import InselectDocument
from inselect.lib.inselect_error import InselectError
from inselect.lib.rect import Rect
from inselect.lib.unicode_csv import UnicodeDictReader
from inselect.lib.utils import make_readonly

from inselect.tests.utils import temp_directory_with_files


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestDocument(unittest.TestCase):
    def test_load(self):
        "Load a document from a file and assertt that properties are as expected"
        path = TESTDATA / 'test_segment.inselect'
        doc = InselectDocument.load(path)

        # Properties are as expected
        self.assertEqual(doc.document_path, path)
        self.assertEqual(5, len(doc.items))
        self.assertEqual(5, doc.n_items)
        self.assertEqual(doc.scanned.path, path.with_suffix('.png'))
        self.assertTrue(doc.thumbnail is None)
        self.assertEqual(TESTDATA / 'test_segment_crops', doc.crops_dir)

        # Check read-only properties
        with self.assertRaises(AttributeError):
            doc.document_path = ''
        with self.assertRaises(AttributeError):
            doc.items = []
        with self.assertRaises(AttributeError):
            doc.crops_dir = ''
        with self.assertRaises(AttributeError):
            doc.n_items = 1

    def _test_load_fails(self, contents):
        """Helper that writes contents to a temp file and asserts that
        InselectDocument.load raises.
        """
        # Temporary files on Windows are pain
        f = tempfile.NamedTemporaryFile(delete=False)
        try:
            f.write(contents)
            f.seek(0)
            f.close()
            self.assertRaises(InselectError, InselectDocument.load, f.name)
        finally:
            os.unlink(f.name)

    def test_load_not_json_document(self):
        self._test_load_fails('XYZ')

    def test_load_not_inselect_document(self):
        self._test_load_fails('{"x": 1}')

    def test_load_bad_version(self):
        self._test_load_fails('{"items": [], "inselect version": 1000}')
        self._test_load_fails('{"items": [], "inselect version": -1}')

    def test_load_images(self):
        "Document's images are loaded as expected"
        source = TESTDATA / 'test_segment.inselect'
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect') as tempdir:
            doc_temp = tempdir / 'test_segment.inselect'
            doc_temp.open('w').write(source.open().read())

            # Document load with no scanned image file
            self.assertRaises(InselectError, InselectDocument.load, doc_temp)

            # Document load with scanned image file present
            scanned_temp = tempdir / 'test_segment.png'
            scanned_temp.open('w')       # File only needs to exist
            actual = InselectDocument.load(doc_temp)
            self.assertEqual(InselectDocument.load(source).items, actual.items)
            self.assertFalse(actual.thumbnail)

            # Document load with scanned and thumbnail files present
            thumbnail_temp = tempdir / 'test_segment_thumbnail.jpg'
            thumbnail_temp.open('w')       # File only needs to exist
            actual = InselectDocument.load(doc_temp)
            self.assertEqual(InselectDocument.load(source).items, actual.items)
            self.assertTrue(actual.thumbnail)

    def test_save(self):
        "Document save writes items"
        source = TESTDATA / 'test_segment.inselect'
        temp = tempfile.mkdtemp()
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:
            items = [ {'fields': {}, 'rect': Rect(0.1, 0.2, 0.5, 0.5) }, ]

            doc_temp = tempdir / 'test_segment.inselect'
            d = InselectDocument.load(doc_temp)
            d.set_items(items)
            d.save()

            self.assertEqual(items, InselectDocument.load(doc_temp).items)

    def test_repr(self):
        path = TESTDATA / 'test_segment.inselect'
        doc = InselectDocument.load(path)
        expected = "InselectDocument ['{0}'] [5 items]".format(str(doc.scanned.path))
        self.assertEqual(expected, repr(doc))

    def test_crops(self):
        "Cropped specimen images are as expected"
        path = TESTDATA / 'test_segment.inselect'
        doc = InselectDocument.load(path)

        self.assertEqual(5, len(doc.items))

        # Check the contents of each crop
        boxes = doc.scanned.from_normalised([i['rect'] for i in doc.items])
        for box, crop in izip(boxes, doc.crops):
            x0, y0, x1, y1 = box.coordinates
            self.assertTrue(np.all(doc.scanned.array[y0:y1, x0:x1] == crop))

    def test_save_crops(self):
        "Cropped specimen images are written correctly"
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:
            doc = InselectDocument.load(tempdir / 'test_segment.inselect')

            crops_dir = doc.save_crops()
            self.assertTrue(crops_dir.is_dir())
            self.assertEqual(crops_dir, doc.crops_dir)
            self.assertEqual(5, len(list(crops_dir.glob('*.png'))))

            # Check the contents of each file
            boxes = doc.scanned.from_normalised([i['rect'] for i in doc.items])
            for box, path in izip(boxes, sorted(crops_dir.glob('*.png'))):
                x0, y0, x1, y1 = box.coordinates
                self.assertTrue(np.all(doc.scanned.array[y0:y1, x0:x1] ==
                                       cv2.imread(str(path))))

    def test_set_items(self):
        "Items are set as expected"
        # TODO LH Check field validation
        path = TESTDATA / 'test_segment.inselect'
        doc = InselectDocument.load(path)

        items = [ {'fields': {}, 'rect': Rect(0, 0, 0.5, 0.5)}, ]
        doc.set_items(items)
        self.assertEqual(items, doc.items)

        # Not normalised
        items = [ {'fields': {}, 'rect': Rect(0, 0, 1, 2)}, ]
        self.assertRaises(InselectError, doc.set_items, items)

    def test_new_from_scan(self):
        "New document is created and saved"
        with temp_directory_with_files(TESTDATA / 'test_segment.png') as tempdir:
            doc = InselectDocument.new_from_scan(tempdir / 'test_segment.png')
            self.assertTrue(doc.document_path.is_file())
            self.assertEqual(tempdir / 'test_segment.png', doc.scanned.path)

    def test_new_from_scan_doc_exists(self):
        "Document of scanned image already exists"
        path = TESTDATA / 'test_segment.png'
        self.assertRaises(InselectError, InselectDocument.new_from_scan, path)

    def test_new_from_thumbnail(self):
        "Can't create a document from a thumbnail image"
        with temp_directory_with_files(TESTDATA / 'test_segment.png') as tempdir:
            doc = InselectDocument.new_from_scan(tempdir / 'test_segment.png')
            doc.ensure_thumbnail(width=2048)
            doc = None

            self.assertRaises(InselectError, InselectDocument.new_from_scan,
                              tempdir / 'test_segment_thumbnail.png')

    def test_new_from_scan_no_image(self):
        "Image does not exist"
        self.assertRaises(InselectError, InselectDocument.new_from_scan, 'i am not a file')

    def test_ensure_thumbnail(self):
        "Thumbnail is created"
        source_doc = TESTDATA / 'test_segment.inselect'
        source_img = TESTDATA / 'test_segment.png'
        with temp_directory_with_files(source_doc, source_img) as tempdir:
            # Document load with no scanned image file
            doc = InselectDocument.load(tempdir / 'test_segment.inselect')
            self.assertTrue(doc.thumbnail is None)
            doc.ensure_thumbnail(width=2048)
            self.assertEqual(2048, doc.thumbnail.array.shape[1])

    def test_ensure_thumbnail_silly_size(self):
        "Can't create thumbnail with a silly size"
        source_doc = TESTDATA / 'test_segment.inselect'
        source_img = TESTDATA / 'test_segment.png'
        with temp_directory_with_files(source_doc, source_img) as tempdir:
            doc = InselectDocument.load(tempdir / 'test_segment.inselect')

            self.assertRaises(InselectError, doc.ensure_thumbnail, -1)
            self.assertRaises(InselectError, doc.ensure_thumbnail, 50)
            self.assertRaises(InselectError, doc.ensure_thumbnail, 20000)

    def test_ensure_thumbnail_read_only(self):
        "Can't write thumbnail to a read-only directory"
        # This case is doing more than simply testing filesystem behavour
        # because it tests the failure code in InselectDocument
        source_doc = TESTDATA / 'test_segment.inselect'
        source_img = TESTDATA / 'test_segment.png'
        with temp_directory_with_files(source_doc, source_img) as tempdir:
            doc = InselectDocument.load(tempdir / 'test_segment.inselect')

            mode = make_readonly(tempdir)

            self.assertRaises(InselectError, doc.ensure_thumbnail)

            # Restor the original mode
            tempdir.chmod(mode)

    def test_csv_export(self):
        "CSV data are exported as expected"
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:
            doc = InselectDocument.load(tempdir / 'test_segment.inselect')
            csv_fname = doc.export_csv()
            self.assertEqual(csv_fname, tempdir / 'test_segment.csv')

            # Check CSV contents
            with csv_fname.open('rb') as f:
                res = UnicodeDictReader(f)
                for index, item, row in izip(count(), doc.items, res):
                    expected = item['fields']
                    expected.update({'Item' : str(1+index)})
                    actual = {k: v for k,v in row.items() if v}
                    self.assertEqual(expected, actual)

    def test_thumbnail_path_of_scanned(self):
        self.assertEqual(Path('x_thumbnail.jpg'),
                         InselectDocument.thumbnail_path_of_scanned('x.png'))


if __name__=='__main__':
    unittest.main()
