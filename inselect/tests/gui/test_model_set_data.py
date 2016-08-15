import unittest

from pathlib import Path

from PySide.QtCore import Qt, QRect

from .gui_test import GUITest

from inselect.lib.document import InselectDocument
from inselect.gui.model import Model
from inselect.gui.roles import RectRole, RotationRole, MetadataRole


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestModelData(GUITest):
    """Test Model's data and setData methods
    """
    def test_set_invalid_rotation(self):
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        i = m.index(0, 0)
        self.assertRaises(ValueError, m.setData, i, 'not an integer', RotationRole)
        self.assertRaises(ValueError, m.setData, i, -1, RotationRole)
        self.assertRaises(ValueError, m.setData, i, 2, RotationRole)

    def test_set_rotation(self):
        "Alter box's rotation"
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        i = m.index(0, 0)
        self.assertEqual(0, m.data(i, RotationRole))

        m.setData(i, 180, RotationRole)
        self.assertEqual(180, m.data(i, RotationRole))

        # Rotation stored 0 <= v < 360
        m.setData(i, -90, RotationRole)
        self.assertEqual(270, m.data(i, RotationRole))

    def test_set_invalid_rect(self):
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        self.assertRaises(ValueError, m.setData, m.index(0, 0), 'not a rect',
                          RectRole)

    def test_set_rect(self):
        "Alter box's rect"
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        i = m.index(0, 0)
        r = QRect(0, 0, 1, 1)
        m.setData(i, r, RectRole)
        self.assertEqual(r, m.data(i, RectRole))

        r = QRect(5, 5, 5, 5)
        m.setData(i, r, RectRole)
        self.assertEqual(r, m.data(i, RectRole))

    def test_set_metadata(self):
        "Alter box's metadata"
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        i = m.index(0, 0)
        expected = {
            "catalogNumber": "1",
            "scientificName": "A",
        }
        self.assertEqual(expected, m.data(i, MetadataRole))

        m.setData(i, {'catalogNumber': '1234'}, MetadataRole)
        expected = {
            "catalogNumber": "1234",
            "scientificName": "A",
        }
        self.assertEqual(expected, m.data(i, MetadataRole))

    def test_set_invalid_index(self):
        m = Model()
        self.assertIsNone(m.data(m.index(-1, -1)))

    def test_set_invalid_metadata(self):
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        self.assertRaises(ValueError, m.setData, m.index(0, 0), 'not a dict',
                          MetadataRole)

    def test_display_role(self):
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        # First four characters only - remainder depend upon current template
        self.assertEqual('0001', m.data(m.index(0, 0), Qt.DisplayRole)[:4])
        self.assertEqual('0003', m.data(m.index(2, 0), Qt.DisplayRole)[:4])
        self.assertEqual('0004', m.data(m.index(3, 0), Qt.DisplayRole)[:4])


if __name__ == '__main__':
    unittest.main()
