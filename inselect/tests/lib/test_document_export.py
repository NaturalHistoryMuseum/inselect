# -*- coding: UTF-8 -*-
import unittest

from itertools import izip
from pathlib import Path

import cv2
import numpy as np
import unicodecsv

from inselect.lib.document import InselectDocument
from inselect.lib.document_export import DocumentExport
from inselect.lib.user_template import UserTemplate

from inselect.tests.utils import temp_directory_with_files

TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestDocumentExportWithTemplate(unittest.TestCase):
    TEMPLATE = UserTemplate({
        'Name': 'Test',
        'Cropped file suffix': '.png',
        'Thumbnail width pixels': 4096,
        'Object label': u'{ItemNumber:02}_{scientificName-value}',
        'Fields': [
            {
                'Name': 'catalogNumber',
            },
            {
                'Name': 'scientificName',
                'Choices with data': [(u'A',         1),
                                      (u'B',         2),
                                      (u'Elsinoë',   3),
                                      (u'D',         4),
                                      (u'インセクト', 10),
                                      ],
            },
        ]
    })

    def test_save_crops(self):
        "Cropped object images are written correctly"
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:
            doc = InselectDocument.load(tempdir / 'test_segment.inselect')

            crops_dir = DocumentExport(self.TEMPLATE).save_crops(doc)

            self.assertTrue(crops_dir.is_dir())
            self.assertEqual(crops_dir, doc.crops_dir)

            cropped_fnames = sorted(crops_dir.glob('*.png'))
            self.assertEqual(
                ['01_1.png', '02_2.png', '03_10.png', '04_3.png', '05_4.png'],
                [f.name for f in cropped_fnames]
            )

            # Check the contents of each file
            boxes = doc.scanned.from_normalised(i['rect'] for i in doc.items)
            for box, path in izip(boxes, sorted(crops_dir.glob('*.png'))):
                x0, y0, x1, y1 = box.coordinates
                self.assertTrue(np.all(doc.scanned.array[y0:y1, x0:x1] ==
                                       cv2.imread(str(path))))

    def test_cancel_save_crops(self):
        "User cancels save crops"
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:
            doc = InselectDocument.load(tempdir / 'test_segment.inselect')

            # Create crops dir with some data
            doc.crops_dir.mkdir()
            with doc.crops_dir.joinpath('a_file').open('w') as outfile:
                outfile.write(u'Some data\n')

            class CancelExport(Exception):
                pass

            def progress(msg):
                "A progress function that cancels the export"
                raise CancelExport()

            self.assertRaises(
                CancelExport,
                DocumentExport(self.TEMPLATE).save_crops, doc, progress=progress
            )

            # Nothing should have changed within tempdir
            self.assertEqual(
                ['test_segment.inselect', 'test_segment.png', doc.crops_dir.name],
                [p.name for p in tempdir.iterdir()])
            self.assertEqual(
                ['a_file'],
                [p.name for p in doc.crops_dir.iterdir()]
            )

    def test_csv_export(self):
        "CSV data are exported as expected"
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:
            doc = InselectDocument.load(tempdir / 'test_segment.inselect')

            csv_path = DocumentExport(self.TEMPLATE).export_csv(doc)
            self.assertEqual(csv_path, tempdir / 'test_segment.csv')

            # Check CSV contents

            with csv_path.open('rb') as f:
                reader = unicodecsv.reader(f, encoding='utf8')
                headers = ['Cropped_image_name', 'ItemNumber', 'catalogNumber',
                           'scientificName', 'scientificName-value']
                self.assertEqual(headers, reader.next())
                self.assertEqual([u'01_1.png',  u'1', u'1', u'A', u'1'], reader.next())
                self.assertEqual([u'02_2.png',  u'2', u'2', u'B', u'2'], reader.next())
                self.assertEqual([u'03_10.png', u'3', u'3', u'インセクト', u'10'],
                                 reader.next())
                self.assertEqual([u'04_3.png',  u'4', u'', u'Elsinoë', u'3'], reader.next())
                self.assertEqual([u'05_4.png',  u'5', u'', u'D', u'4'], reader.next())
                self.assertIsNone(next(reader, None))


class TestCropFnameCollision(unittest.TestCase):
    TEMPLATE = UserTemplate({
        'Name': 'Test',
        'Cropped file suffix': '.png',
        'Thumbnail width pixels': 4096,
        'Object label': u'{scientificName}',
        'Fields': [
            {
                'Name': 'scientificName'
            }
        ]
    })

    def test_fname_collison(self):
        "Duplicated crop fnames have numerical suffixes to avoid collisions"
        class FakeDocument(object):
            pass

        document = FakeDocument()
        document.items = [
            {
                "fields": {
                    "scientificName": "A"
                },
            }, {
                "fields": {
                    "scientificName": "A"
                },
            }, {
                "fields": {
                    "scientificName": "A"
                },
            }, {
                "fields": {
                    "scientificName": "D"
                },
            }, {
                "fields": {
                    "scientificName": "B"
                },
            }, {
                "fields": {
                    "scientificName": "D"
                },
            }, {
                "fields": {
                    "scientificName": "A"
                },
            }
        ]

        fnames = list(DocumentExport(self.TEMPLATE).crop_fnames(document))
        self.assertEqual(
            ['A.png', 'A-1.png', 'A-2.png', 'D.png', 'B.png', 'D-1.png', 'A-3.png'],
            fnames
        )


if __name__ == '__main__':
    unittest.main()
