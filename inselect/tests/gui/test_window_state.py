import unittest

from PySide.QtCore import QCoreApplication, QSize

from gui_test import GUITest


class TestPersistWindowState(GUITest):
    """The main window's size, position and state - maximized and full screen
    """
    @classmethod
    def setUpClass(cls):
        super(TestPersistWindowState, cls).setUpClass()

        # The QSettings default constructor uses the application's
        # organizationName and applicationName properties.
        QCoreApplication.setOrganizationName('NHM')
        QCoreApplication.setApplicationName('inselect')

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

    def test_show_size(self):
        "Show with size"
        w = self.window

        w.showNormal()
        w.show_with_size(QSize(300, 400))
        self.assertEqual(QSize(300, 400), w.size())

        w.show_with_size(QSize(800, 600))
        self.assertEqual(QSize(800, 600), w.size())


if __name__ == '__main__':
    unittest.main()
