import unittest

from itertools import izip
from pathlib import Path

from PySide.QtCore import QSettings

from inselect.gui.recent_documents import RecentDocuments

from gui_test import MainWindowTest


class TestRecentDocuments(MainWindowTest):
    """Tests the recent documents and associated menu items
    """
    def setUp(self):
        super(TestRecentDocuments, self).setUp()

        # Clear recent documents
        QSettings().remove(RecentDocuments.KEY)

    def test_no_recent_documents(self):
        "No recent documents"
        self.assertEqual([], RecentDocuments().read_paths())
        w = self.window
        w._sync_recent_documents_actions()

        self.assertFalse(w.recent_doc_actions[0].isEnabled())
        self.assertTrue(w.recent_doc_actions[0].isVisible())
        self.assertEqual('No recent documents', w.recent_doc_actions[0].text())

        self.assertFalse(w.recent_doc_actions[1].isVisible())

    def test_single_recent_document(self):
        "A single recent document"
        RecentDocuments().add_path('x')
        w = self.window
        w._sync_recent_documents_actions()

        self.assertTrue(w.recent_doc_actions[0].isEnabled())
        self.assertTrue(w.recent_doc_actions[0].isVisible())
        self.assertEqual('x', w.recent_doc_actions[0].text())

        self.assertFalse(w.recent_doc_actions[1].isVisible())

    def test_maximum_number_of_recent_documents(self):
        "The maximum number of recent documents"
        paths = ['a', 'b', 'c', 'd', 'e']
        paths = [Path(p) for p in paths]

        # Add paths in reverse order so that 'a' is the most recent
        for path in reversed(paths):
            RecentDocuments().add_path(path)

        self.assertEqual(paths, RecentDocuments().read_paths())

        self.window._sync_recent_documents_actions()
        for expected, action in izip(paths, self.window.recent_doc_actions):
            self.assertTrue(action.isEnabled())
            self.assertTrue(action.isVisible())
            self.assertEqual(str(expected), action.text())

    def test_limit_recent_documents(self):
        """Add a recent document when at capacity
        """
        # Add six paths
        paths = ['f', 'e', 'd', 'c', 'b', 'a']
        paths = [Path(p) for p in paths]

        # Add paths in reverse order so that 'f' is the most recent
        for path in reversed(paths):
            RecentDocuments().add_path(path)

        # Should contain just the first 5 elements
        self.assertEqual(paths[:5], RecentDocuments().read_paths())

        w = self.window
        w._sync_recent_documents_actions()

        self.assertEqual('f', w.recent_doc_actions[0].text())

    def test_add_existing(self):
        "Add a recent document that is already in the list"
        p = Path('x')
        RecentDocuments().add_path(p)
        RecentDocuments().add_path(p)
        RecentDocuments().add_path(p)

        self.assertEqual([p], RecentDocuments().read_paths())


if __name__ == '__main__':
    unittest.main()
