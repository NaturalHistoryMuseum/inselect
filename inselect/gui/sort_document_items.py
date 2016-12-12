from PyQt5.QtCore import QSettings

from inselect.lib.sort_document_items import sort_document_items

# QSettings path
_PATH = 'sort_by_columns'

# Global - set to instance of CookieCutterChoice in cookie_cutter_boxes
_SORT_DOCUMENT = None


def sort_items_choice():
    "Returns an instance of SortDocumentItems"
    global _SORT_DOCUMENT
    if not _SORT_DOCUMENT:
        _SORT_DOCUMENT = SortDocumentItems()
    return _SORT_DOCUMENT


class SortDocumentItems(object):
    def __init__(self):
        # Key holds an integer
        self._by_columns = 1 == QSettings().value(_PATH, 0)

    @property
    def by_columns(self):
        """The user's preference for ordering by columns (True) or by rows
        (False)
        """
        return self._by_columns

    def sort_items(self, items, by_columns):
        """Returns items sorted by columns (True) or by rows (False) or by the
        user's most recent preference (None).
        """
        self._by_columns = by_columns
        # Pass integer to setValue - calling setValue with a bool with result
        # in a string being written to the QSettings store.
        QSettings().setValue(_PATH, 1 if by_columns else 0)
        return sort_document_items(items, by_columns)
