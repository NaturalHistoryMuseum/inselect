import unittest

from collections import OrderedDict
from pathlib import Path

from inselect.lib.user_template import UserTemplate

TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestUserTemplate(unittest.TestCase):
    TEMPLATE = UserTemplate({
        'Name': 'T1',
        'Fields': [{'Name': 'F1'}],
        'Cropped file suffix': '.tiff',
        'Thumbnail width pixels': 5000,
        'Object label': '{ItemNumber:03}-{First}-{Second}-{Second-value}-{Last}',
        'Fields':
        [
            {
                'Name': 'First',
                'Mandatory': True,
                'Choices': ['A', 'B']
            },
            {
                'Name': 'Second',
                'Choices with data': OrderedDict([('ABC', 0),
                                                  ('DEF', 1),
                                                  ]),
            },
            {
                'Name': 'Third',
                'Parser': 'int'
            },
            {
                'Name': 'Last',
                'Regex parser': '^[0-9]{9}$'
            },
        ],
    })

    def test_str_repr(self):
        t = self.TEMPLATE
        self.assertEqual('UserTemplate [T1] with 4 fields', str(t))
        self.assertEqual('<UserTemplate [T1] with 4 fields>', repr(t))

    def test_properties(self):
        t = self.TEMPLATE
        self.assertEqual('T1', t.name)
        self.assertEqual('.tiff', t.cropped_file_suffix)
        self.assertEqual(5000, t.thumbnail_width_pixels)
        self.assertEqual(4, len(t.fields))

        self.assertEqual('First', t.fields[0].name)
        self.assertTrue(t.fields[0].mandatory)
        self.assertEqual(['A', 'B'], t.fields[0].choices)
        self.assertIsNone(t.fields[0].choices_with_data)
        self.assertIsNone(t.fields[0].parse_fn)

        self.assertEqual('Second', t.fields[1].name)
        self.assertFalse(t.fields[1].mandatory)
        self.assertIsNone(t.fields[1].choices)
        self.assertEqual(OrderedDict([('ABC', 0), ('DEF', 1)]),
                         t.fields[1].choices_with_data)
        self.assertIsNone(t.fields[1].parse_fn)

        self.assertEqual('Third', t.fields[2].name)
        self.assertTrue(t.fields[2].parse_fn)

        self.assertEqual('Last', t.fields[3].name)
        self.assertTrue(t.fields[3].parse_fn)

    def test_field_names(self):
        t = self.TEMPLATE
        self.assertEqual(['ItemNumber', 'First', 'Second', 'Second-value',
                          'Third', 'Last'], list(t.field_names()))

    def test_format_label(self):
        t = self.TEMPLATE
        metadata = {'Second': 'DEF', 'Last': '22'}
        self.assertEqual('010--DEF-1-22', t.format_label(10, metadata))

    def test_validate_field_mandatory(self):
        t = self.TEMPLATE
        self.assertTrue(t.validate_field('Second', 'ABC'))
        self.assertTrue(t.validate_field('Not a field', '123'))
        self.assertFalse(t.validate_field('First', ''))
        self.assertTrue(t.validate_field('First', 'A'))

    def test_validate_field_parser(self):
        t = self.TEMPLATE
        self.assertTrue(t.validate_field('Third', ''))
        self.assertFalse(t.validate_field('Third', 'x'))
        self.assertTrue(t.validate_field('Third', '123'))

    def test_validate_field_parser_regex(self):
        t = self.TEMPLATE
        self.assertTrue(t.validate_field('Last', ''))
        self.assertFalse(t.validate_field('Last', '12345678'))
        self.assertTrue(t.validate_field('Last',  '123456789'))

    def test_validate_metadata_fail_parse(self):
        t = self.TEMPLATE
        self.assertTrue(t.validate_metadata({'First': 'A', 'Third': ''}))
        self.assertFalse(t.validate_metadata({'First': 'A', 'Third': 'xyz'}))
        self.assertTrue(t.validate_metadata({'First': 'A', 'Third': '0'}))
        self.assertTrue(t.validate_metadata({'First': 'A', 'Third': '1'}))

    def test_validate_metadata_missing_mandatory(self):
        t = self.TEMPLATE
        self.assertFalse(t.validate_metadata({'First': ''}))
        self.assertTrue(t.validate_metadata({'First': 'A'}))

    def test_validate_not_in_choices(self):
        t = self.TEMPLATE
        self.assertFalse(t.validate_metadata({'First': 'xyz'}))
        self.assertFalse(t.validate_metadata({'Second': 'xyz'}))

    def test_from_file(self):
        "Load from a YAML file"
        doc = UserTemplate.load(TESTDATA / 'test.inselect_template')
        self.assertEqual(doc.name, "Test user template")
        self.assertEqual(doc.cropped_file_suffix, '.jpg')
        self.assertEqual(doc.thumbnail_width_pixels, 4096)
        self.assertEqual(3, len(doc.fields))
        self.assertEqual('catalogNumber', doc.fields[0].name)
        self.assertEqual('Location', doc.fields[1].name)
        self.assertEqual('Taxonomy', doc.fields[2].name)


if __name__ == '__main__':
    unittest.main()
