import unittest

from pathlib import Path

from PySide import QtGui

from gui_test import MainWindowTest

TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestViews(MainWindowTest):
    """Basic tests of the boxes and objects views. Functions test as much of the
    view's paint methods as possible by loading a document, selecting the view
    under test and showing the main window full screen.
    """

    def test_boxes_view_paint(self):
        "Boxes view is painted"
        self.window.open_file(TESTDATA / 'test_segment.inselect')
        self.window.showFullScreen()
        self.run_event_loop()

    def test_objects_view_grid_paint(self):
        "Objects grid view is painted"
        self.window.open_file(TESTDATA / 'test_segment.inselect')
        self.window.show_tab(1)
        self.window.show_grid()
        self.window.showFullScreen()
        self.run_event_loop()

    def test_objects_view_expanded_paint(self):
        "Objects expanded view is painted"
        self.window.open_file(TESTDATA / 'test_segment.inselect')
        self.window.show_tab(1)
        self.window.show_expanded()
        self.window.showFullScreen()
        self.run_event_loop()


if __name__=='__main__':
    unittest.main()
