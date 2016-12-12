import unittest

from pathlib import Path

from .gui_test import GUITest


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestActiveView(GUITest):
    """Basic tests of the MainWindow's active view.
    """

    def test_select_view(self):
        "Different views are selected"
        self.window.show_tab(index=0)
        self.assertEqual(0, self.window.views.currentIndex())

        self.window.show_tab(index=1)
        self.assertEqual(1, self.window.views.currentIndex())

        self.window.show_tab(index=0)
        self.assertEqual(0, self.window.views.currentIndex())

    def test_select_next_tab(self):
        "Next tab is selected"
        self.window.show_tab(index=0)
        self.window.next_previous_tab(next=True)
        self.assertEqual(1, self.window.views.currentIndex())

        # Next again moves to first tab
        self.window.next_previous_tab(next=True)
        self.assertEqual(0, self.window.views.currentIndex())

        # Previous moves back to last tab
        self.window.next_previous_tab(next=False)
        self.assertEqual(1, self.window.views.currentIndex())

        self.window.next_previous_tab(next=False)
        self.assertEqual(0, self.window.views.currentIndex())


    def test_close(self):
        "User closes document and Inselect shows Boxes tab"
        self.window.open_file(path=TESTDATA.joinpath('shapes.inselect'))
        self.window.show_tab(index=1)
        self.window.close()
        self.assertEqual(0, self.window.views.currentIndex())


if __name__ == '__main__':
    unittest.main()
