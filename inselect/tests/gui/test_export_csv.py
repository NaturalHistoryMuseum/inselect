import unittest

from itertools import izip, count
from mock import patch
from pathlib import Path

from PySide.QtGui import QMessageBox

from gui_test import MainWindowTest

from inselect.lib.unicode_csv import UnicodeDictReader

from inselect.tests.utils import temp_directory_with_files


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestExportCSV(MainWindowTest):
    """Metadata CSV files are written
    """
    def _test_csv(self):
        doc = self.window.document
        csv = doc.document_path.with_suffix('.csv')

        # Check CSV contents
        with csv.open('rb') as f:
            res = UnicodeDictReader(f)
            for index, item, row in izip(count(), doc.items, res):
                expected = item['fields']
                expected.update({'Item': '{0}'.format(1+index),
                                 'Cropped_image_name': '{0:04}.png'.format(1+index),
                                })
                actual = {k: v for k,v in row.items() if v}
                self.assertEqual(expected, actual)

        # Expect 4 rows
        self.assertEqual(index, 4)

    @patch.object(QMessageBox, 'information', return_value=QMessageBox.Yes)
    def test_export_no_existing_csv(self, mock_information):
        "User exported CSV"
        w = self.window

        # Load document and write the CSV file
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:

            # Load document and export CSV file
            w.open_document(tempdir / 'test_segment.inselect')
            w.export_csv(use_metadata_template=False)
            self._test_csv()

            # User should have been told about the export
            self.assertTrue(mock_information.called)
            expected = u"Data for 5 boxes written to {0}"
            expected = expected.format(tempdir / 'test_segment.csv')
            self.assertTrue(expected in mock_information.call_args[0])

    @patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes)
    @patch.object(QMessageBox, 'information', return_value=QMessageBox.Yes)
    def test_export_overwite_existing_csv(self, mock_information, mock_question):
        "User wants to overwrite existing CSV file"
        w = self.window

        # Load document and write the CSV file
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:

            # Create a CSV file to force the GUI to prompt for over-write
            (tempdir / 'test_segment.csv').open('w')

            # Load document and export CSV file
            w.open_document(tempdir / 'test_segment.inselect')
            w.export_csv(use_metadata_template=False)
            self._test_csv()

            # User should have been told about the export
            self.assertTrue(mock_information.called)
            expected = u"Data for 5 boxes written to {0}"
            expected = expected.format(tempdir / 'test_segment.csv')
            self.assertTrue(expected in mock_information.call_args[0])

            # User should have been prompted to overwrite the existing file
            self.assertTrue(mock_question.called)
            question = 'Overwrite the existing CSV file?'
            self.assertTrue(question in mock_question.call_args[0])

    @patch.object(QMessageBox, 'question', return_value=QMessageBox.No)
    @patch.object(QMessageBox, 'information', return_value=QMessageBox.Yes)
    def test_export_do_not_overwite_existing_csv(self, mock_information, mock_question):
        "User does not want to overwrite existing CSV file"
        w = self.window

        # Load document and write the CSV file
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:

            # Create a CSV file to force the GUI to prompt for over-write
            (tempdir / 'test_segment.csv').open('w')

            # Load document and export CSV file
            w.open_document(tempdir / 'test_segment.inselect')
            w.export_csv()

            # File should not have been altered
            self.assertEqual('', (tempdir / 'test_segment.csv').open().read())

            # User should not have been told about the export
            self.assertFalse(mock_information.called)

            # User should have been prompted to overwrite the existing file
            self.assertTrue(mock_question.called)
            question = 'Overwrite the existing CSV file?'
            self.assertTrue(question in mock_question.call_args[0])


if __name__=='__main__':
    unittest.main()
