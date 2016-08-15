import unittest

from pathlib import Path

from inselect.gui.user_template_choice import user_template_choice
from inselect.gui.views.metadata import FieldEdit, FieldComboBox

from .gui_test import GUITest

TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestMetadataViewControls(GUITest):
    """Controls in the metadata view reflect the selected template
    """
    def setUp(self):
        super(TestMetadataViewControls, self).setUp()
        t = user_template_choice()
        t.load(TESTDATA / 'test.inselect_template')

    def test_template_name(self):
        self.assertEqual('Test user template',
                         self.window.view_metadata.popup_button.text())

    def test_controls(self):
        controls = self.window.view_metadata._form_container.controls
        # controls is a dict { control: field name }
        self.assertEqual(3, len(controls))
        self.assertIn('catalogNumber', list(controls.values()))
        self.assertIn('Location', list(controls.values()))
        self.assertIn('Taxonomy', list(controls.values()))

    def _control_for_field(self, field):
        "Returns the control for the given field"
        f = self.window.view_metadata._form_container
        # f.controls is a dict { control: field name }
        for key, value in f.controls.items():
            if field == value:
                return key
        else:
            raise ValueError('No field [{0}]'.format(field))

    def test_catalog_number(self):
        catalog_number = self._control_for_field('catalogNumber')
        self.assertIsInstance(catalog_number, FieldEdit)
        self.assertEqual('catalogNumber', catalog_number._field)
        # Display name is a URLField
        self.assertIn('<a href="http://rs.tdwg.org/dwc/terms/catalogNumber">Catalog number</a>',
                      catalog_number.previousInFocusChain().text())

    def test_location(self):
        location = self._control_for_field('Location')
        self.assertIsInstance(location, FieldComboBox)
        self.assertEqual('Location', location._field)
        self.assertEqual('Location', location.previousInFocusChain().text())
        self.assertEqual(5, location.count())
        self.assertEqual('', location.itemText(0))
        self.assertIsNone(location.itemData(0))
        self.assertEqual('Drawer X', location.itemText(1))
        self.assertEqual('NA', location.itemData(1))
        self.assertEqual('Drawer 1', location.itemText(2))
        self.assertEqual('123', location.itemData(2))
        self.assertEqual('Drawer 2', location.itemText(3))
        self.assertEqual('456', location.itemData(3))
        self.assertEqual('Drawer 3', location.itemText(4))
        self.assertEqual('789', location.itemData(4))

    def test_taxonomy(self):
        location = self._control_for_field('Taxonomy')
        self.assertIsInstance(location, FieldComboBox)
        self.assertEqual('Taxonomy', location._field)
        self.assertEqual('Taxonomy', location.previousInFocusChain().text())
        self.assertEqual(5, location.count())
        self.assertEqual('', location.itemText(0))
        self.assertIsNone(location.itemData(0))
        self.assertEqual('Plesiosauria', location.itemText(1))
        self.assertIsNone(location.itemData(1))
        self.assertEqual('Attenborosaurus', location.itemText(2))
        self.assertIsNone(location.itemData(2))
        self.assertEqual('Elasmosaurus', location.itemText(3))
        self.assertIsNone(location.itemData(3))
        self.assertEqual('Styxosaurus', location.itemText(4))
        self.assertIsNone(location.itemData(4))


if __name__ == '__main__':
    unittest.main()
