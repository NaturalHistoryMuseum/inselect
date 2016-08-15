# -*- coding: UTF-8 -*-
import unittest


from operator import itemgetter
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
        'Object label': '{ItemNumber:02}_{scientificName-value}',
        'Fields': [
            {
                'Name': 'catalogNumber',
            },
            {
                'Name': 'scientificName',
                'Choices with data': [('A',         1),
                                      ('B',         2),
                                      ('Elsinoë',   3),
                                      ('D',         4),
                                      ('インセクト', 10),
                                      ],
            },
        ]
    })

    def test_save_crops(self):
        "Cropped object images are written correctly"
        with temp_directory_with_files(TESTDATA / 'shapes.inselect',
                                       TESTDATA / 'shapes.png') as tempdir:
            doc = InselectDocument.load(tempdir / 'shapes.inselect')

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
            for box, path in zip(boxes, sorted(crops_dir.glob('*.png'))):
                x0, y0, x1, y1 = box.coordinates
                self.assertTrue(np.all(doc.scanned.array[y0:y1, x0:x1] ==
                                       cv2.imread(str(path))))

    def test_cancel_save_crops(self):
        "User cancels save crops"
        with temp_directory_with_files(TESTDATA / 'shapes.inselect',
                                       TESTDATA / 'shapes.png') as tempdir:
            doc = InselectDocument.load(tempdir / 'shapes.inselect')

            # Create crops dir with some data
            doc.crops_dir.mkdir()
            with doc.crops_dir.joinpath('a_file').open('w') as outfile:
                outfile.write('Some data\n')

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
                ['shapes.inselect', 'shapes.png', doc.crops_dir.name],
                sorted(p.name for p in tempdir.iterdir()))
            self.assertEqual(
                ['a_file'],
                [p.name for p in doc.crops_dir.iterdir()]
            )

    def test_csv_export(self):
        "CSV data are exported as expected"
        with temp_directory_with_files(TESTDATA / 'shapes.inselect',
                                       TESTDATA / 'shapes.png') as tempdir:
            doc = InselectDocument.load(tempdir / 'shapes.inselect')

            csv_path = DocumentExport(self.TEMPLATE).export_csv(doc)
            self.assertEqual(csv_path, tempdir / 'shapes.csv')

            # Check CSV contents

            with csv_path.open('rb') as f:
                reader = unicodecsv.reader(f, encoding='utf8')
                headers = [
                    'Cropped_image_name', 'ItemNumber',
                    'NormalisedLeft', 'NormalisedTop', 'NormalisedRight',
                    'NormalisedBottom', 'ThumbnailLeft', 'ThumbnailTop',
                    'ThumbnailRight', 'ThumbnailBottom', 'OriginalLeft',
                    'OriginalTop', 'OriginalRight', 'OriginalBottom',
                    'catalogNumber', 'scientificName', 'scientificName-value'
                ]
                self.assertEqual(headers, next(reader))

                # Check only the metadata columns and 'original' coordinates
                # columns, ignoring thumbnail (which doesn't exist)
                # and normalised (which are floating point) coordinates
                metadata_cols = itemgetter(0, 1, 10, 11, 12, 13, 14, 15, 16)
                self.assertEqual(
                    ('01_1.png', '1',
                     '0', '0', '189', '189',
                     '1', 'A', '1'),
                    metadata_cols(next(reader))
                )
                self.assertEqual(
                    ('02_2.png', '2',
                     '271', '0', '459', '189',
                     '2', 'B', '2'),
                    metadata_cols(next(reader))
                )
                self.assertEqual(
                    ('03_10.png', '3',
                     '194', '196', '257', '232',
                     '3', 'インセクト', '10'),
                    metadata_cols(next(reader))
                )
                self.assertEqual(
                    ('04_3.png', '4',
                     '0', '248', '189', '437',
                     '4', 'Elsinoë', '3'),
                    metadata_cols(next(reader))
                )
                self.assertEqual(
                    ('05_4.png', '5',
                     '271', '248', '459', '437',
                     '5', 'D', '4'),
                    metadata_cols(next(reader))
                )
                self.assertIsNone(next(reader, None))


class TestCropFnameCollision(unittest.TestCase):
    TEMPLATE = UserTemplate({
        'Name': 'Test',
        'Cropped file suffix': '.png',
        'Thumbnail width pixels': 4096,
        'Object label': '{scientificName}',
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
