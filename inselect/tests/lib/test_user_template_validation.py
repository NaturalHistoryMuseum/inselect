import unittest

from inselect.lib.user_template import (validate_specification,
                                        UserTemplate, InvalidSpecificationError)


class TestValidateUserTemplate(unittest.TestCase):
    """Tests the validation of user templates
    """
    def _invalid_specification(self, specification):
        """Asserts that 'specification' is invalid and returns a list of
        validation problems
        """
        with self.assertRaises(InvalidSpecificationError) as invalid:
            validate_specification(specification)
        return invalid.exception.problems

    def test_no_name(self):
        self.assertIn('No template name', self._invalid_specification({}))

    def test_name_not_a_string(self):
        self.assertIn('Template name should be a string',
                      self._invalid_specification({'Name': 1}))

    def test_invalid_cropped_file_suffix(self):
        spec = {'Cropped file suffix' : 'I am not a valid file suffix',}
        res = self._invalid_specification(spec)
        expected = ('Invalid "Cropped file suffix" [I am not a valid file '
                    'suffix]. Must be one of [.bmp, .jpeg, .jpg, .png, .tif, '
                    '.tiff]')
        self.assertIn(expected, res)

    def test_unrecognised_cropped_file_suffix(self):
        spec = {'Cropped file suffix' : '.txt',}
        res = self._invalid_specification(spec)
        expected = ('Invalid "Cropped file suffix" [.txt]. Must be one of '
                    '[.bmp, .jpeg, .jpg, .png, .tif, .tiff]')
        self.assertIn(expected, res)

    def test_invalid_thumbnail_width(self):
        spec = {'Thumbnail width pixels' : 10,}
        res = self._invalid_specification(spec)
        expected = ('Invalid "Thumbnail width pixels" [10]. Must be between '
                    '[1024] and [16384]')
        self.assertIn(expected, res)

    def test_no_fields(self):
        self.assertIn('No fields defined', self._invalid_specification({}))

    def test_missing_field_name(self):
        res = self._invalid_specification({'Fields': [{}]})
        self.assertIn('One or more fields do not have a name', res)

    def test_illegal_field_name(self):
        res = self._invalid_specification({'Fields': [{'Name': 'ItemNumber'}]})
        self.assertIn("Fields cannot be called ['ItemNumber']", res)

    def test_duplicated_field_names(self):
        spec = {'Fields': [
            {'Name': 'First'},
            {'Name': 'First'},
            {'Name': 'Second'},
            {'Name': 'Second'},
        ]}
        res = self._invalid_specification(spec)
        self.assertIn('Duplicated field name [First]', res)
        self.assertIn('Duplicated field name [Second]', res)

    def test_empty_labels(self):
        spec = {'Fields': [
            {'Name': 'F1', 'Label': ''},
        ]}
        res = self._invalid_specification(spec)
        self.assertIn('Empty label for [F1]', res)

    def test_duplicated_labels(self):
        spec = {'Fields': [
            {'Name': 'F1', 'Label': 'Tooth length'},
            {'Name': 'F2', 'Label': 'Tooth length'},
        ]}
        res = self._invalid_specification(spec)
        self.assertIn('Duplicated label [Tooth length]', res)

    def test_choices_and_choices_with_data(self):
        "Both Choices and Choices with data given"
        spec = {'Fields': [
            {'Name': 'F', 'Choices': [], 'Choices with data': {}},
        ]}
        res = self._invalid_specification(spec)
        expected = 'Both "Choices" and "Choices with data" given for [F]'
        self.assertIn(expected, res)

    def test_duplicated_choices(self):
        "Choices contains duplicated values"
        spec = {'Fields': [
            {'Name': 'F', 'Choices': ['A', 'A']},
        ]}
        res = self._invalid_specification(spec)
        expected = 'Duplicated "Choices" for [F]: [A]'
        self.assertIn(expected, res)

    def test_empty_choices(self):
        spec = {'Fields': [
            {'Name': 'F', 'Choices': []},
        ]}
        res = self._invalid_specification(spec)
        expected = u'Empty "Choices" for [F]'
        self.assertIn(expected, res)

    def test_empty_choices_with_data(self):
        spec = {'Fields': [
            {'Name': 'F', 'Choices with data': {}},
        ]}
        res = self._invalid_specification(spec)
        expected = u'Empty "Choices with data" for [F]'
        self.assertIn(expected, res)

    def test_choices_with_data_clash(self):
        "A field name clashes with a 'Choices with data' value field"
        spec = {'Fields': [
            {'Name': 'F2-value'},
            {'Name': 'F2', 'Choices with data': {}},
        ]}
        res = self._invalid_specification(spec)
        expected = u'A field named "F2-value" cannot be defined'
        self.assertIn(expected, res)

    def test_empty_parser(self):
        spec = {'Fields': [
            {'Name': 'F1', 'Parser': ''},
        ]}
        res = self._invalid_specification(spec)
        expected = ('Unrecognised parser for [F1]: []')
        self.assertIn(expected, res)

    def test_unrecognised_parser(self):
        spec = {'Fields': [
            {'Name': 'F1', 'Parser': 'Not a parser'},
        ]}
        res = self._invalid_specification(spec)
        expected = ('Unrecognised parser for [F1]: [Not a parser]')
        self.assertIn(expected, res)

    def test_parser_and_parserregex(self):
        spec = {'Fields': [
            {'Name': 'F1', 'Parser': 'parse_int', "Regex parser": '[0-9]+'},
        ]}
        res = self._invalid_specification(spec)
        expected = ('Both "Parser" and "Regex parser" given for [F1]')
        self.assertIn(expected, res)

    def test_user_template_two_validation_errors(self):
        with self.assertRaises(InvalidSpecificationError) as cm:
            UserTemplate({})

        self.assertEqual('2 problems:\nNo template name\nNo fields defined',
                         str(cm.exception))
        self.assertEqual(['No template name', 'No fields defined'],
                         cm.exception.problems)

    def test_user_template_one_validation_error(self):
        with self.assertRaises(InvalidSpecificationError) as cm:
            UserTemplate({'Name': 'T1'})

        self.assertEqual('1 problem:\nNo fields defined', str(cm.exception))
        self.assertEqual(['No fields defined'], cm.exception.problems)


if __name__=='__main__':
    unittest.main()
