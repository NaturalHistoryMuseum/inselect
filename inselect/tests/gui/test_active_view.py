import unittest

from .gui_test import GUITest


class TestActiveView(GUITest):
    """Basic tests of the MainWindow's active view.
    """

    def test_select_boxes_view(self):
        "Boxes view is selected"
        self.window.show_tab(0)
        self.assertEqual(0, self.window.views.currentIndex())

    def test_select_objects_view(self):
        "Objects view is selected"
        self.window.show_tab(1)
        self.assertEqual(1, self.window.views.currentIndex())

    def test_select_next_tab(self):
        "Next tab is selected"
        self.window.show_tab(0)
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


if __name__ == '__main__':
    unittest.main()
