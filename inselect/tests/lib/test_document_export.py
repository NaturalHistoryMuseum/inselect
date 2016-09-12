# -*- coding: UTF-8 -*-
import unittest

from itertools import izip
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
        'Object label': u'{ItemNumber:02}_{scientificName-value}',
        'Fields': [
            {
                'Name': 'catalogNumber',
            },
            {
                'Name': 'Department',
                'Fixed value': 'Entomology',
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
            for box, path in izip(boxes, sorted(crops_dir.glob('*.png'))):
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
                    'catalogNumber', 'Department', 'scientificName',
                    'scientificName-value'
                ]
                self.assertEqual(headers, reader.next())

                # Check only the metadata columns and 'original' coordinates
                # columns, ignoring thumbnail (which doesn't exist)
                # and normalised (which are floating point) coordinates
                metadata_cols = itemgetter(0, 1, 10, 11, 12, 13, 14, 15, 16, 17)
                self.assertEqual(
                    (u'01_1.png', u'1',
                     u'0', u'0', u'189', u'189',
                     u'1', u'Entomology', u'A', u'1'),
                    metadata_cols(reader.next())
                )
                self.assertEqual(
                    (u'02_2.png', u'2',
                     u'271', u'0', u'459', u'189',
                     u'2', u'Entomology', u'B', u'2'),
                    metadata_cols(reader.next())
                )
                self.assertEqual(
                    (u'03_10.png', u'3',
                     u'194', u'196', u'257', u'232',
                     u'3', u'Entomology', u'インセクト', u'10'),
                    metadata_cols(reader.next())
                )
                self.assertEqual(
                    (u'04_3.png', u'4',
                     u'0', u'248', u'189', u'437',
                     u'4', u'Entomology', u'Elsinoë', u'3'),
                    metadata_cols(reader.next())
                )
                self.assertEqual(
                    (u'05_4.png', u'5',
                     u'271', u'248', u'459', u'437',
                     u'5', u'Entomology', u'D', u'4'),
                    metadata_cols(reader.next())
                )
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
