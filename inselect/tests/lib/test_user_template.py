import unittest

from collections import OrderedDict

from inselect.lib.user_template import UserTemplate

from inselect.lib.parse import parse_int


class TestUserTemplate(unittest.TestCase):
    def test_str_repr(self):
        spec = {'Name': 'T1', 'Fields': [{'Name': 'F1'},],
               }
        t = UserTemplate(spec)
        self.assertEqual('UserTemplate [T1] with 1 fields', str(t))
        self.assertEqual('<UserTemplate [T1] with 1 fields>', repr(t))

    def test_properties(self):
        spec = {'Name': 'T1',
                'Fields': [{'Name': 'F1'},],
                'Cropped file suffix': '.tiff',
                'Thumbnail width pixels': 5000,
                'Fields' : [{'Name': 'F1', 'Mandatory': True, 'Choices': ['A','B']},
                            {'Name': 'F2',
                             'Choices with data': OrderedDict([('A', 1), ('B', 2)]),
                            }
                           ]
               }
        t = UserTemplate(spec)
        self.assertEqual('T1', t.name)
        self.assertEqual('.tiff', t.cropped_file_suffix)
        self.assertEqual(5000, t.thumbnail_width_pixels)
        self.assertEqual(2, len(t.fields))
        self.assertEqual('F1', t.fields[0].name)
        self.assertTrue(t.fields[0].mandatory)
        self.assertEqual(['A','B'], t.fields[0].choices)
        self.assertIsNone(t.fields[0].choices_with_data)
        self.assertIsNone(t.fields[0].parse_fn)
        self.assertEqual('F2', t.fields[1].name)
        self.assertFalse(t.fields[1].mandatory)
        self.assertIsNone(t.fields[1].choices)
        self.assertEqual(OrderedDict([('A', 1), ('B', 2)]),
                         t.fields[1].choices_with_data)
        self.assertIsNone(t.fields[1].parse_fn)

    def test_field_names(self):
        spec = {'Name': 'T1',
                'Fields': [{'Name': 'First'},
                           {'Name': 'Second',
                            'Choices with data' : OrderedDict([('ABC', 0)]),
                           },
                           {'Name': 'Last'},
                          ],
               }
        t = UserTemplate(spec)
        self.assertEqual(['ItemNumber', 'First', 'Second', 'Second-value', 'Last'],
                         list(t.field_names()))

    def test_format_label(self):
        spec = {'Name': 'T1',
                'Fields': [{'Name': 'First'},
                           {'Name': 'Second',
                            'Choices with data' : OrderedDict([('ABC', 0),
                                                               ('DEF', 1)
                                                              ]),
                           },
                           {'Name': 'Last'},
                          ],
                'Object label': '{ItemNumber:03}-{First}-{Second}-{Second-value}-{Last}',
               }
        t = UserTemplate(spec)
        metadata = {'Second': 'DEF', 'Last': '22'}
        self.assertEqual('010--DEF-1-22', t.format_label(10, metadata))

    def test_validate_field_mandatory(self):
        spec = {'Name': 'T1',
                'Fields': [{'Name': 'First', 'Mandatory': True,},
                           {'Name': 'Second'},
                          ],
               }
        t = UserTemplate(spec)
        self.assertTrue(t.validate_field('Second', '123'))
        self.assertTrue(t.validate_field('Not a field', '123'))
        self.assertFalse(t.validate_field('First', ''))
        self.assertTrue(t.validate_field('First', ' '))
        self.assertTrue(t.validate_field('First', '123'))

    def test_validate_field_parser(self):
        spec = {'Name': 'T1',
                'Fields': [{'Name': 'First', 'Parser': 'int'}],
               }
        t = UserTemplate(spec)
        self.assertTrue(t.validate_field('First', ''))
        self.assertFalse(t.validate_field('First', 'x'))
        self.assertTrue(t.validate_field('First', '123'))

    def test_validate_field_parser_regex(self):
        spec = {'Name': 'T1',
                'Fields': [{'Name': 'First', 'Regex parser': '^[0-9]{9}$'}],
               }
        t = UserTemplate(spec)
        self.assertTrue(t.validate_field('First', ''))
        self.assertFalse(t.validate_field('First', '12345678'))
        self.assertTrue(t.validate_field('First', '123456789'))

    def test_validate_metadata_fail_parse(self):
        spec = {'Name': 'T1',
                'Fields': [{'Name': 'First', 'Parser': 'int_gt0'}],
               }
        t = UserTemplate(spec)
        self.assertTrue(t.validate_metadata({'First': ''}))
        self.assertFalse(t.validate_metadata({'First': 'xyz'}))
        self.assertFalse(t.validate_metadata({'First': '0'}))
        self.assertTrue(t.validate_metadata({'First': '1'}))

    def test_validate_metadata_missing_mandatory(self):
        spec = {'Name': 'T1',
                'Fields': [{'Name': 'First', 'Mandatory': True}],
               }
        t = UserTemplate(spec)
        self.assertFalse(t.validate_metadata({'First': ''}))
        self.assertTrue(t.validate_metadata({'First': ' '}))
        self.assertTrue(t.validate_metadata({'First': 'xyz'}))


if __name__=='__main__':
    unittest.main()
