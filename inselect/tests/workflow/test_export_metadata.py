import unittest

from itertools import izip, count
from pathlib import Path

import unicodecsv

from inselect.lib.document import InselectDocument

from inselect.workflow.export_metadata import export_csv

from inselect.tests.utils import temp_directory_with_files


TESTDATA = Path(__file__).parent.parent / 'test_data'


# TODO LH Many more tests required

class TestExportCSV(unittest.TestCase):
    def test_export_csv(self):
        "Export metadata to CSV"
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:

            export_csv(tempdir, overwrite_existing=False)

            csv = tempdir / 'test_segment.csv'
            self.assertTrue(csv.is_file())

            # Check CSV contents
            doc = InselectDocument.load(tempdir / 'test_segment.inselect')
            with csv.open('rb') as f:
                res = unicodecsv.DictReader(f, encoding='utf-8')
                for index, item, row in izip(count(), doc.items, res):
                    expected = item['fields']
                    expected.update({
                        'ItemNumber': str(1+index),
                        'Cropped_image_name': '{0:04}.jpg'.format(1+index)
                    })
                    actual = {k: v for k, v in row.items() if v}
                    self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
