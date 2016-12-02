import unittest

from pathlib import Path

from qtpy.QtCore import QRect

from .gui_test import GUITest

from inselect.lib.document import InselectDocument
from inselect.gui.model import Model
from inselect.gui.roles import RectRole, RotationRole, MetadataRole


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestModelData(GUITest):
    """Test Model's insertRows and removeRows methods
    """
    def test_insert_invalid_rows(self):
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        self.assertEqual(5, m.rowCount())
        self.assertRaises(ValueError, m.insertRows, -1, 1)   # -ve row
        self.assertRaises(ValueError, m.insertRows,  6, 1)   # row > n existing rows
        self.assertRaises(ValueError, m.insertRows,  0, -1)  # -ve count

    def test_insert_rows(self):
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        self.assertEqual(5, m.rowCount())
        m.insertRows(5, 2)

        self.assertEqual(7, m.rowCount())

        i = m.index(5, 0)
        self.assertEqual({}, m.data(i, MetadataRole))
        self.assertEqual(0, m.data(i, RotationRole))
        self.assertEqual(QRect(0, 0, 0, 0), m.data(i, RectRole))

        i = m.index(6, 0)
        self.assertEqual({}, m.data(i, MetadataRole))
        self.assertEqual(0, m.data(i, RotationRole))
        self.assertEqual(QRect(0, 0, 0, 0), m.data(i, RectRole))

    def test_insert_row(self):
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        self.assertEqual(5, m.rowCount())
        m.insertRow(5)

        self.assertEqual(6, m.rowCount())

        i = m.index(5, 0)
        self.assertEqual({}, m.data(i, MetadataRole))
        self.assertEqual(0, m.data(i, RotationRole))
        self.assertEqual(QRect(0, 0, 0, 0), m.data(i, RectRole))

    def test_remove_invalid_rows(self):
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        self.assertEqual(5, m.rowCount())
        self.assertRaises(ValueError, m.removeRows, -1, 1)   # -ve row
        self.assertRaises(ValueError, m.removeRows,  6, 1)   # row > n existing rows
        self.assertRaises(ValueError, m.removeRows,  0, -1)  # -ve count

    def test_remove_rows(self):
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        m.removeRows(0, 1)
        self.assertEqual(4, m.rowCount())
        expected = {"catalogNumber": "2", "scientificName": "B"}
        self.assertEqual(expected, m.data(m.index(0, 0), MetadataRole))


if __name__ == '__main__':
    unittest.main()
