import unittest

from mock import patch
from pathlib import Path

from PySide.QtCore import QLocale
from PySide.QtGui import QApplication

from inselect.app import main
from inselect.gui.main_window import MainWindow

TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestApp(unittest.TestCase):
    """Start and exit the application
    """
    @classmethod
    def tearDown(self):
        "Close the top-level window that was created in main()"
        for w in filter(lambda o: isinstance(o, MainWindow),
                        QApplication.topLevelWidgets()):
            w.close()

    @patch.object(QApplication, 'exec_', return_value=0)
    def test_app(self, mock_exec_):
        "User starts the application"
        self.assertRaises(SystemExit, main, [])
        self.assertTrue(mock_exec_.called)

    @unittest.skip('Causes segfault')
    @patch.object(QApplication, 'exec_', return_value=0)
    @patch.object(MainWindow, 'open_file')
    def test_app_load_file(self, mock_open_file, mock_exec_):
        "User starts the application with a file"
        path = str(TESTDATA / 'test_segment.inselect')
        self.assertRaises(SystemExit, main, ['path to executable', path])
        self.assertTrue(mock_exec_.called)
        mock_open_file.assert_called_once_with(path)

    @patch.object(QApplication, 'exec_', return_value=0)
    @patch.object(QLocale, 'setDefault')
    def test_app_set_locale(self, mock_set_default, mock_exec_):
        "User starts the application with a non-default locale"
        locale = 'ja_JP'
        self.assertRaises(SystemExit, main, ['path to executable', '-l', locale])
        self.assertTrue(mock_exec_.called)
        mock_set_default.assert_called_once_with(locale)


if __name__ == '__main__':
    unittest.main()
