import unittest

from itertools import izip, count
from pathlib import Path

import unicodecsv

from inselect.lib.document import InselectDocument

from inselect.workflow.export_metadata import main

from inselect.tests.utils import temp_directory_with_files


TESTDATA = Path(__file__).parent.parent / 'test_data'


# TODO LH Many more tests required

class TestExportCSV(unittest.TestCase):
    def test_export_csv_with_existing(self):
        "Attempt to export metadata over an existing CSV file"
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:

            # Create CSV file
            csv = tempdir / 'test_segment.csv'
            with csv.open('w') as outfile:
                outfile.write(u'This is only a test\n')

            main([unicode(tempdir)])

            # File should not have been altered
            with csv.open('r') as infile:
                res = infile.read()
            self.assertEqual('This is only a test\n', res)

    def test_export_csv(self):
        "Export metadata to CSV"
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:

            # Create an empty CSV file
            csv = tempdir / 'test_segment.csv'
            with csv.open('w'):
                pass

            main([unicode(tempdir), '--overwrite'])

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
