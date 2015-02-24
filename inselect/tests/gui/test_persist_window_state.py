import unittest
from pathlib import Path

from gui_test import GUITest

from PySide import QtGui

TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestPersistWindowState(GUITest):
    """The main window's size, position and state - maximized and full screen
    """
    def test_full_screen_persisted(self):
        w = self.window

        w.showNormal()
        w.showFullScreen()
        w.write_geometry_settings()

        w.showNormal()
        self.assertFalse(w.isMaximized())

        w.show_from_geometry_settings()
        self.assertTrue(w.isFullScreen())

    def test_maximized_persisted(self):
        w = self.window

        w.showNormal()
        w.showMaximized()
        w.write_geometry_settings()

        w.showNormal()
        self.assertFalse(w.isMaximized())

        w.show_from_geometry_settings()
        self.assertTrue(w.isMaximized())

    def test_normal_persisted(self):
        w = self.window

        w.showNormal()
        pos, size = w.pos(), w.size()
        w.write_geometry_settings()

        w.showMaximized()
        self.assertTrue(w.isMaximized())

        w.show_from_geometry_settings()
        self.assertFalse(w.isMaximized())
        self.assertEqual(pos, w.pos())
        self.assertEqual(size, w.size())


if __name__=='__main__':
    unittest.main()
