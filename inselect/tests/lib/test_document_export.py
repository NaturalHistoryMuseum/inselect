# -*- coding: UTF-8 -*-
import unittest

from itertools import izip, count
from pathlib import Path

import cv2
import numpy as np

from inselect.lib.document import InselectDocument
from inselect.lib.document_export import DocumentExport
from inselect.lib.user_template import UserTemplate
from inselect.lib.templates.dwc import DWC
from inselect.lib.unicode_csv import UnicodeReader, UnicodeDictReader

from inselect.tests.utils import temp_directory_with_files

TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestDocumentExportWithTemplate(unittest.TestCase):
    TEMPLATE = UserTemplate({
        'Name': 'Test',
        'Cropped file suffix': '.png',
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

            print('xx', list(self.TEMPLATE.field_names()))
            crops_dir = DocumentExport(self.TEMPLATE).save_crops(doc)
            print('zzz', self.TEMPLATE.metadata(1, {"scientificName": "A"}))

            self.assertTrue(crops_dir.is_dir())
            self.assertEqual(crops_dir, doc.crops_dir)

            cropped_fnames = sorted(crops_dir.glob('*.png'))
            self.assertEqual(['01_1.png', '02_2.png', '03_10.png', '04_3.png', '05_4.png'],
                             [f.name for f in cropped_fnames])

            # Check the contents of each file
            boxes = doc.scanned.from_normalised([i['rect'] for i in doc.items])
            for box, path in izip(boxes, sorted(crops_dir.glob('*.png'))):
                x0, y0, x1, y1 = box.coordinates
                self.assertTrue(np.all(doc.scanned.array[y0:y1, x0:x1] ==
                                       cv2.imread(str(path))))

    def test_csv_export(self):
        "CSV data are exported as expected"
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:
            doc = InselectDocument.load(tempdir / 'test_segment.inselect')

            csv_path = DocumentExport(self.TEMPLATE).export_csv(doc)
            self.assertEqual(csv_path, tempdir / 'test_segment.csv')

            # Check CSV contents

            with csv_path.open('rb') as f:
                reader = UnicodeReader(f)
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


if __name__=='__main__':
    unittest.main()
