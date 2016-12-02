import unittest

from mock import create_autospec
from pathlib import Path

from qtpy.QtCore import QRect

from .gui_test import GUITest

from inselect.lib.document import InselectDocument
from inselect.gui.model import Model
from inselect.gui.roles import RectRole, RotationRole, MetadataRole

from inselect.tests.utils import temp_directory_with_files


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestModelModified(GUITest):
    """Tests the modified state of the model
    """
    def _new_mock_modified_changed(self, model):
        "Returns a mock function connected to model's modified_changed signal"
        def modified_changed():
            pass
        f = create_autospec(modified_changed)
        model.modified_changed.connect(f)
        return f

    def test_new_document_not_modified(self):
        "Open a document - expect it not show as modified"
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))
        self.assertFalse(m.is_modified)

    def test_set_rotation_modifies(self):
        "Alter box's rotation"
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        mock_modified_changed = self._new_mock_modified_changed(m)
        m.setData(m.index(0, 0), 90, RotationRole)
        mock_modified_changed.assert_called_once_with()
        self.assertTrue(m.is_modified)

    def test_set_same_rotation_does_not_modify(self):
        "Set box's rotation to the same value as it currently has"
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        mock_modified_changed = self._new_mock_modified_changed(m)
        m.setData(m.index(0, 0), 0, RotationRole)
        self.assertFalse(mock_modified_changed.called)
        self.assertFalse(m.is_modified)

    def test_set_rect_modifies(self):
        "Alter box's rect"
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        mock_modified_changed = self._new_mock_modified_changed(m)
        m.setData(m.index(0, 0), QRect(0, 0, 1, 1), RectRole)
        mock_modified_changed.assert_called_once_with()
        self.assertTrue(m.is_modified)

    def test_set_same_rect_does_not_modify(self):
        "Set box's rect with the same value as it currently has"
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        mock_modified_changed = self._new_mock_modified_changed(m)
        m.setData(m.index(0, 0), m.data(m.index(0, 0), RectRole), RectRole)
        self.assertFalse(mock_modified_changed.called)
        self.assertFalse(m.is_modified)

    def test_set_metadata_modifies(self):
        "Alter box's metadata"
        m = Model()
        m.from_document(InselectDocument.load(TESTDATA / 'shapes.inselect'))

        mock_modified_changed = self._new_mock_modified_changed(m)
        m.setData(m.index(0, 0), {'catalogNumber': None}, MetadataRole)
        mock_modified_changed.assert_called_once_with()
        self.assertTrue(m.is_modified)

    def test_modified_cleared(self):
        "Alter document and clear"
        with temp_directory_with_files(TESTDATA / 'shapes.inselect',
                                       TESTDATA / 'shapes.png') as tempdir:
            m = Model()
            m.from_document(InselectDocument.load(tempdir / 'shapes.inselect'))

            # Alter data
            mock_modified_changed = self._new_mock_modified_changed(m)
            m.setData(m.index(0, 0), -90, RotationRole)
            mock_modified_changed.assert_called_once_with()
            self.assertTrue(m.is_modified)

            # Clear
            m.clear()

            self.assertEqual(2, mock_modified_changed.call_count)
            self.assertFalse(m.is_modified)


if __name__ == '__main__':
    unittest.main()
