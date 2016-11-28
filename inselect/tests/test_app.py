import locale
import unittest

from mock import patch
from pathlib import Path

from qtpy.QtCore import QLocale
from qtpy.QtWidgets import QApplication

from inselect.app import main
from inselect.gui.main_window import MainWindow

TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestApp(unittest.TestCase):
    """Start and exit the application
    """
    @patch.object(QApplication, 'exec_', return_value=0)
    def test_app(self, mock_exec_):
        "User starts the application"
        self.assertRaises(SystemExit, main, [])
        self.assertTrue(mock_exec_.called)

    @patch.object(QApplication, 'exec_', return_value=0)
    @patch.object(MainWindow, 'open_file')
    def test_app_load_file(self, mock_open_file, mock_exec_):
        "User starts the application with a file"
        path = str(TESTDATA / 'shapes.inselect')
        self.assertRaises(SystemExit, main, [path])
        self.assertTrue(mock_exec_.called)
        mock_open_file.assert_called_once_with(Path(path))

    @patch.object(QApplication, 'exec_', return_value=0)
    @patch.object(QLocale, 'setDefault')
    @patch.object(locale, 'setlocale')
    def test_app_set_locale(self, mock_setlocale, mock_set_default, mock_exec_):
        "User starts the application with a non-default locale"
        # Python's locale.setlocale raises an exception if the locale is
        # unrecognised, so it is mocked.
        loc = 'ja_JP'
        self.assertRaises(SystemExit, main, ['-l', loc])
        self.assertTrue(mock_exec_.called)
        mock_set_default.assert_called_once_with(QLocale(loc))
        # Other actions inside main might cause setlocale to be called so
        # should not assert number of calls.
        mock_setlocale.assert_any_call(locale.LC_ALL, loc)


if __name__ == '__main__':
    unittest.main()
