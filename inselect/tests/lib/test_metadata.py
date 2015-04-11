import unittest

from inselect.lib.metadata import MetadataTemplate
from inselect.lib.templates.price import template as price
from inselect.lib.templates.dwc import template as dwc


class TestMetadataTemplateSpec(unittest.TestCase):
    "MetadataTemplate enforces specification"
    def test_missing_template_name(self):
        spec = {'Fields': [{'Name': 'a'}]}
        self.assertRaises(ValueError, MetadataTemplate, spec)

    def test_bad_cropped_file_suffix(self):
        spec = {'Name': 'test',
                'Fields': [{'Name': 'a'}],
                'Cropped file suffix': 'xx',
               }
        self.assertRaises(ValueError, MetadataTemplate, spec)

    def test_no_fields(self):
        self.assertRaises(ValueError, MetadataTemplate, {'Name': 'test'})

    def test_no_field_name(self):
        spec = {'Name': 'test',
                'Fields': [{'Choices': ['x', 'y', 'z']}],
               }
        self.assertRaises(ValueError, MetadataTemplate, spec)

    def test_duplicated_fields(self):
        spec = {'Name': 'test',
                'Fields': [{'Name': 'a'},
                           {'Name': 'a'},]
               }
        self.assertRaises(ValueError, MetadataTemplate, spec)

    def test_empty_choices(self):
        spec = {'Name': 'test',
                'Fields': [{'Name': 'a', 'Choices': []}]
               }
        self.assertRaises(ValueError, MetadataTemplate, spec)

    def test_duplicated_choices(self):
        spec = {'Name': 'test',
                'Fields': [{'Name': 'a', 'Choices': ['x', 'x']}]
               }
        self.assertRaises(ValueError, MetadataTemplate, spec)

    def test_empty_choices_with_data(self):
        spec = {'Name': 'test',
                'Fields': [{'Name': 'a', 'ChoicesWithData': []}]
               }
        self.assertRaises(ValueError, MetadataTemplate, spec)

    def test_duplicated_choices_with_data(self):
        spec = {'Name': 'test',
                'Fields': [{'Name': 'a',
                            'ChoicesWithData': [ ('x', 1), ('x', 1)]},
                          ]
               }
        self.assertRaises(ValueError, MetadataTemplate, spec)

    def test_choices_with_data_value(self):
        spec = {'Name': 'test',
                'Fields': [{'Name': 'a',
                            'ChoicesWithData': [ ('x', 1), ('y', 2)]},
                           {'Name': 'a-value'},
                          ],
               }
        self.assertRaises(ValueError, MetadataTemplate, spec)

    def test_choices_and_choices_with_data(self):
        spec = {'Name': 'test',
                'Fields': [{'Name' : 'a',
                            'Choices': ['x', 'y'],
                            'ChoicesWithData': [ ('x', 1), ('y', 2)]},
                ]}
        self.assertRaises(ValueError, MetadataTemplate, spec)


class TestMetadataTemplate(unittest.TestCase):
    TEST = MetadataTemplate({
        'Name': 'Test',
        'Cropped file suffix': '.jpg',
        'Object label': u'{First}_{Third}_{Third-value}',
        'Fields': [
            {
                'Name': 'First'
            },
            {
                'Name': 'Second',
                'Choices': ['x', 'y', 'z']
            },
            {
                'Name': 'Third',
                'Mandatory': True,
                'ChoicesWithData': [('a', 1),
                                    ('b', 2),
                                    ('c', 3),
                                    ],
            },
            {
                'Name': 'Fourth',
                'Parser': int,
            },
        ]
    })

    def test_repr(self):
        self.assertEqual('<MetadataTemplate [Test] with 4 fields>', repr(self.TEST))

    def test_str(self):
        self.assertEqual('MetadataTemplate [Test] with 4 fields', str(self.TEST))

    def test_name(self):
        self.assertEqual('Test', self.TEST.name)

    def test_cropped_image_suffix(self):
        self.assertEqual('.jpg', self.TEST.cropped_image_suffix)

    def test_mandatory(self):
        self.assertEqual(['Third'], self.TEST.mandatory)

    def test_box_metadata(self):
        box = {'fields': 
            {
                'First': 'abc',
                'Second': 'xyz',
                'Third': 'a',
                'Fourth': '1',
            }
        }
        expected = box['fields']
        expected.update({'Third-value': 1})
        self.assertEqual(expected, self.TEST.box_metadata(box))

    def test_box_metadata_value_not_in_choices(self):
        "Label is not in the 'ChoicesWithData' list"
        box = {'fields': 
            {
                'First': 'abc',
                'Second': 'xyz',
                'Third': 'd',
                'Fourth': '1',
            }
        }
        self.assertEqual(box['fields'], self.TEST.box_metadata(box))

    def test_format_label_all_fields(self):
        box = {'fields': 
            {
                'First': 'abc',
                'Second': 'xyz',
                'Third': 'a',
            }
        }
        self.assertEqual('abc_a_1', self.TEST.format_label(box))

    def test_format_label_value_not_in_choices(self):
        "Label is not in the 'ChoicesWithData' list"
        box = {'fields': 
            {
                'First': 'x',
                'Third': 'd',
            }
        }
        self.assertEqual('x_d_', self.TEST.format_label(box))

    def test_format_label_no_values(self):
        box = {'fields': {}}
        self.assertEqual('__', self.TEST.format_label(box))

    def test_validate_box(self):
        box = {'fields': {'Third': 'a', 'Fourth': '1'}}
        self.assertTrue(self.TEST.validate_box(box))

    def test_validate_box_mandatory_not_given(self):
        box = {'fields': {'Fourth': '1'}}
        self.assertFalse(self.TEST.validate_box(box))

    def test_validate_box_fail_parse(self):
        box = {'fields': {'Third': 'a', 'Fourth': 'xxx'}}
        self.assertFalse(self.TEST.validate_box(box))

    def test_validate_field_unknown_field(self):
        "A field that the template does not know about"
        self.assertTrue(self.TEST.validate_field('xxx', ''))

    def test_validate_field_mandatory_given(self):
        self.assertTrue(self.TEST.validate_field('Third', 'a'))

    def test_validate_field_mandatory_not_given(self):
        self.assertFalse(self.TEST.validate_field('Third', ''))

    def test_validate_field_parse_ok(self):
        self.assertTrue(self.TEST.validate_field('Fourth', '1'))

    def test_validate_field_parse_fail(self):
        self.assertFalse(self.TEST.validate_field('Fourth', 'x'))


if __name__=='__main__':
    unittest.main()
