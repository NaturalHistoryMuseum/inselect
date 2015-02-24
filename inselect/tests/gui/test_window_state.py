import unittest
from pathlib import Path

from PySide import QtGui

from gui_test import GUITest

TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestPersistWindowState(GUITest):
    """The main window's size, position and state - maximized and full screen
    """
    def test_full_screen_persisted(self):
        "Full-screen state persisted correctly"
        w = self.window

        w.showNormal()
        w.showFullScreen()
        self.assertFalse(w.isMaximized())
        self.assertTrue(w.isFullScreen())

        w.write_geometry_settings()

        w.showNormal()
        self.assertFalse(w.isMaximized())
        self.assertFalse(w.isFullScreen())

        w.show_from_geometry_settings()
        self.assertTrue(w.isFullScreen())

    def test_maximized_persisted(self):
        "Maximized state persisted correctly"
        w = self.window

        w.showNormal()
        w.showMaximized()
        self.assertTrue(w.isMaximized())
        self.assertFalse(w.isFullScreen())

        w.write_geometry_settings()

        w.showNormal()
        self.assertFalse(w.isMaximized())
        self.assertFalse(w.isFullScreen())

        w.show_from_geometry_settings()
        self.assertTrue(w.isMaximized())

    def test_normal_persisted(self):
        "Normal state persisted correctly"
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

    def test_toggle_fullscreen(self):
        "Full-screen state toggle"
        w = self.window

        w.showNormal()
        w.toggle_full_screen()
        self.assertTrue(w.isFullScreen())

        w.toggle_full_screen()
        self.assertFalse(w.isFullScreen())

if __name__=='__main__':
    unittest.main()
