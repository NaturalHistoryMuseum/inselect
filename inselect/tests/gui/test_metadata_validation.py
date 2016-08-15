import unittest

from mock import patch
from pathlib import Path

from PySide.QtGui import QMessageBox

from .gui_test import GUITest

from inselect.gui.roles import MetadataRole
from inselect.lib.user_template import UserTemplate


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestMetadataValidation(GUITest):
    @patch.object(QMessageBox, 'setText')
    @patch.object(QMessageBox, 'setDetailedText')
    @patch.object(QMessageBox, 'exec_', return_value=QMessageBox.No)
    def test_save_crops_invalid_document(self, mock_question, mock_setdetailed,
                                         mock_settext):
        """The user wants to export crops for a document with many validation
        failures
        """
        w = self.window

        # This document has 15 validation problems with this template
        w.open_document(TESTDATA / 'shapes.inselect')
        template = UserTemplate.load(TESTDATA / 'test.inselect_template')

        w.save_crops(user_template=template)

        # Close the document
        self.assertTrue(w.close_document())

        # Should have been called
        self.assertEqual(1, mock_settext.call_count)
        self.assertIn('The document contains 15 validation problems',
                      mock_settext.call_args[0][0])

        # Detailed text should not have been given
        self.assertEqual(1, mock_setdetailed.call_count)

    @patch.object(QMessageBox, 'setText')
    @patch.object(QMessageBox, 'setDetailedText')
    @patch.object(QMessageBox, 'exec_', return_value=QMessageBox.No)
    def test_export_csv_invalid_document(self, mock_question, mock_setdetailed,
                                         mock_settext):
        """The user wants to export to CSV for a document with a single
        validation failure
        """
        w = self.window

        w.open_document(TESTDATA / 'shapes.inselect')

        template = UserTemplate({
            'Name': 'T1',
            'Fields': [{'Name': 'F1'}],
            'Cropped file suffix': '.jpg',
            'Thumbnail width pixels': 5000,
            'Object label': '{catalogNumber}',
        })

        # Set the catalogNumber for each box to the same value, creating a
        # single validation problem
        for index in (w.model.index(row, 0) for row in range(5)):
            w.model.setData(index, {'catalogNumber': '1234'}, MetadataRole)

        w.export_csv(user_template=template)

        # Close the document
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            self.assertTrue(self.window.close_document())

        # Should have been called
        self.assertEqual(1, mock_settext.call_count)
        self.assertIn('The document contains 1 validation problems',
                      mock_settext.call_args[0][0])

        # Detailed text should not have been given
        self.assertEqual(0, mock_setdetailed.call_count)


if __name__ == '__main__':
    unittest.main()
