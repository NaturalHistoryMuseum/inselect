import unittest
import shutil
import tempfile

from mock import patch
from pathlib import Path

from cv2 import imread

from PySide.QtGui import QFileDialog

from gui_test import GUITest


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestSaveScreengrab(GUITest):
    """Tests saving of a screengrab
    """
    def test_save_screengrab_with_doc(self):
        "User saves a screengrab with a document loaded"
        self.window.open_file(TESTDATA / 'shapes.inselect')

        temp = tempfile.mkdtemp()
        try:
            img_path = Path(temp) / 'shapes_screengrab.png'
            with patch.object(QFileDialog, 'getSaveFileName',
                              return_value=(str(img_path), '.png')) as mock_file_dialog:
                self.window.save_screengrab()
                self.assertTrue(mock_file_dialog.called)
                self.assertTrue(img_path.is_file())

            # Check that the file is an image
            self.assertTrue(imread(str(img_path)) is not None)

        finally:
            shutil.rmtree(temp)

    def test_save_screengrab_no_doc(self):
        "User saves a screengrab without a document loaded"
        temp = tempfile.mkdtemp()
        try:
            img_path = Path(temp) / 'inselect_screengrab.png'
            with patch.object(QFileDialog, 'getSaveFileName',
                              return_value=(str(img_path), '.png')) as mock_file_dialog:
                self.window.save_screengrab()
                self.assertTrue(mock_file_dialog.called)
                self.assertTrue(img_path.is_file())

            # Check that the file is an image
            self.assertTrue(imread(str(img_path)) is not None)
        finally:
            shutil.rmtree(temp)

    def test_cancel_save_screengrab(self):
        "User cancels the save screengrab box"
        temp = tempfile.mkdtemp()
        try:
            img_path = Path(temp) / 'inselect_screengrab.png'
            with patch.object(QFileDialog, 'getSaveFileName',
                              return_value=('', '')) as mock_file_dialog:
                self.window.save_screengrab()
                self.assertTrue(mock_file_dialog.called)
                self.assertFalse(img_path.is_file())
        finally:
            shutil.rmtree(temp)


if __name__ == '__main__':
    unittest.main()
