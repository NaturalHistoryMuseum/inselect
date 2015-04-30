import unittest
import shutil

from itertools import count
from pathlib import Path

from inselect.lib.document import InselectDocument
from inselect.lib.unicode_csv import UnicodeDictReader

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
                res = UnicodeDictReader(f)
                for index, item, row in zip(count(), doc.items, res):
                    expected = item['fields']
                    expected.update({'Item' : str(1+index)})
                    actual = {k: v for k,v in list(row.items()) if v}
                    self.assertEqual(expected, actual)


if __name__=='__main__':
    unittest.main()
