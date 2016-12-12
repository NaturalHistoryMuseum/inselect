import unittest

from itertools import count
from mock import patch
from pathlib import Path

import unicodecsv

from PyQt5.QtWidgets import QMessageBox

from .gui_test import GUITest
from inselect.lib.persist_user_template import BOUNDING_BOX_FIELD_NAMES
from inselect.lib.templates.dwc import DWC
from inselect.tests.utils import temp_directory_with_files


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestExportCSV(GUITest):
    """Metadata CSV files are written
    """
    def _test_csv(self):
        doc = self.window.document
        csv = doc.document_path.with_suffix('.csv')

        # Check CSV contents
        with csv.open('rb') as f:
            res = unicodecsv.DictReader(f, encoding='utf-8')
            for index, item, row in zip(count(), doc.items, res):
                expected = item['fields']
                expected.update({
                    'ItemNumber': '{0}'.format(1 + index),
                    'Cropped_image_name': '{0:04}.jpg'.format(1 + index),
                })
                actual = {k: v for k, v in list(row.items()) if v and k not in BOUNDING_BOX_FIELD_NAMES}
                self.assertEqual(expected, actual)

        # Expect 4 rows
        self.assertEqual(index, 4)

    @patch.object(QMessageBox, 'information', return_value=QMessageBox.Yes)
    def test_export_no_existing_csv(self, mock_information):
        "User exported CSV"
        w = self.window

        # Load document and write the CSV file
        with temp_directory_with_files(TESTDATA / 'shapes.inselect',
                                       TESTDATA / 'shapes.png') as tempdir:

            # Load document and export CSV file
            w.open_document(path=tempdir / 'shapes.inselect')
            w.export_csv(user_template=DWC)
            self._test_csv()

            # User should have been told about the export
            self.assertTrue(mock_information.called)
            expected = "Data for 5 boxes written to {0}"
            expected = expected.format(tempdir / 'shapes.csv')
            self.assertTrue(expected in mock_information.call_args[0])

    @patch.object(QMessageBox, 'question', return_value=QMessageBox.Yes)
    @patch.object(QMessageBox, 'information', return_value=QMessageBox.Yes)
    def test_export_overwite_existing_csv(self, mock_information, mock_question):
        "User wants to overwrite existing CSV file"
        w = self.window

        # Load document and write the CSV file
        with temp_directory_with_files(TESTDATA / 'shapes.inselect',
                                       TESTDATA / 'shapes.png') as tempdir:

            # Create a CSV file to force the GUI to prompt for over-write
            (tempdir / 'shapes.csv').open('w')

            # Load document and export CSV file
            w.open_document(path=tempdir / 'shapes.inselect')
            w.export_csv(user_template=DWC)
            self._test_csv()

            # User should have been told about the export
            self.assertTrue(mock_information.called)
            expected = "Data for 5 boxes written to {0}"
            expected = expected.format(tempdir / 'shapes.csv')
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
        with temp_directory_with_files(TESTDATA / 'shapes.inselect',
                                       TESTDATA / 'shapes.png') as tempdir:

            # Create a CSV file to force the GUI to prompt for over-write
            (tempdir / 'shapes.csv').open('w')

            # Load document and export CSV file
            w.open_document(tempdir / 'shapes.inselect')
            w.export_csv(user_template=DWC)

            # File should not have been altered
            self.assertEqual('', (tempdir / 'shapes.csv').open().read())

            # User should not have been told about the export
            self.assertFalse(mock_information.called)

            # User should have been prompted to overwrite the existing file
            self.assertTrue(mock_question.called)
            question = 'Overwrite the existing CSV file?'
            self.assertTrue(question in mock_question.call_args[0])


if __name__ == '__main__':
    unittest.main()
