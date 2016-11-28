import unittest

from functools import partial
from mock import patch
from pathlib import Path

import cv2

from qtpy.QtWidgets import QMessageBox

from inselect.lib.templates.dwc import DWC
from inselect.tests.utils import temp_directory_with_files

from gui_test import GUITest


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestSaveCrops(GUITest):
    @patch.object(QMessageBox, 'information', return_value=QMessageBox.Yes)
    @patch.object(QMessageBox, 'warning', return_value=QMessageBox.Ok)
    def test_save_crops(self, mock_warning, mock_information):
        "The user saves crops using DWC template"
        with temp_directory_with_files(TESTDATA / 'shapes.inselect',
                                       TESTDATA / 'shapes.png') as tempdir:
            self.window.open_document(path=tempdir / 'shapes.inselect')

            crops_dir = tempdir / 'shapes_crops'
            self.assertFalse(crops_dir.is_dir())
            self.run_async_operation(
                partial(self.window.save_crops, user_template=DWC)
            )

            self.assertTrue(crops_dir.is_dir())
            self.assertEqual(5, len(list(crops_dir.iterdir())))

            self.assertTrue(mock_information.called)
            expected = '5 crops saved in {0}'.format(crops_dir)
            self.assertTrue(expected in mock_information.call_args[0])

            # User should not have been warned about missing scanned image
            self.assertFalse(mock_warning.called)

    @patch.object(QMessageBox, 'information', return_value=QMessageBox.Yes)
    @patch.object(QMessageBox, 'warning', return_value=QMessageBox.Ok)
    def test_save_crops_overwrite(self, mock_warning, mock_information):
        "The user is prompted to overwrite existing crops"
        with temp_directory_with_files(TESTDATA / 'shapes.inselect',
                                       TESTDATA / 'shapes.png') as tempdir:
            self.window.open_document(path=tempdir / 'shapes.inselect')

            crops_dir = tempdir / 'shapes_crops'
            crops_dir.mkdir()
            self.assertTrue(crops_dir.is_dir())

            # Answer with 'no'
            with patch.object(QMessageBox, 'question',
                              return_value=QMessageBox.No) as mock_question:
                self.window.save_crops(user_template=DWC)
                expected = 'Overwrite the existing object images?'
                self.assertTrue(expected in mock_question.call_args[0])

            # Crops dir still contains no files
            self.assertTrue(crops_dir.is_dir())
            self.assertEqual(0, len(list(crops_dir.iterdir())))

            # Confirmation of saving crops was not shown
            self.assertFalse(mock_information.called)

            # Answer with 'no'
            with patch.object(QMessageBox, 'question',
                              return_value=QMessageBox.Yes) as mock_question:
                self.run_async_operation(
                    partial(self.window.save_crops, user_template=DWC)
                )
                expected = 'Overwrite the existing object images?'
                self.assertTrue(expected in mock_question.call_args[0])

            # Five crops written
            self.assertTrue(crops_dir.is_dir())
            self.assertEqual(5, len(list(crops_dir.iterdir())))

            # Confirmation of saving crops was shown
            self.assertTrue(mock_information.called)

            # User should not have been warned about missing scanned image
            self.assertFalse(mock_warning.called)

    @patch.object(QMessageBox, 'warning', return_value=QMessageBox.Ok)
    def test_save_crops_no_scanned_image(self, mock_warning):
        "The user is informed that there is no scanned image"
        with temp_directory_with_files(TESTDATA / 'shapes.inselect') as tempdir:
            # Create thumbnail file
            img = cv2.imread(str(TESTDATA.joinpath('shapes.png')))
            cv2.imwrite(str(tempdir.joinpath('shapes_thumbnail.jpg')), img)
            self.window.open_document(path=tempdir / 'shapes.inselect')

            crops_dir = tempdir / 'shapes_crops'
            self.assertFalse(crops_dir.is_dir())

            self.window.save_crops(user_template=DWC)

            expected = ('Unable to save crops because the original '
                        'full-resolution image file does not exist.')
            self.assertTrue(expected in mock_warning.call_args[0])

            # Crops should not have been written
            self.assertFalse(crops_dir.is_dir())


if __name__ == '__main__':
    unittest.main()
