import unittest

from pathlib import Path

from inselect.lib.persist_user_template import (user_template_from_specification,
                                                InvalidSpecificationError)


class TestValidateUserTemplate(unittest.TestCase):
    """Tests the validation of user templates
    """
    def _invalid_specification(self, specification):
        """Asserts that 'specification' is invalid and returns a list of
        validation problems
        """
        with self.assertRaises(InvalidSpecificationError) as invalid:
            user_template_from_specification(specification)
        return invalid.exception.problems

    def test_no_name(self):
        self.assertIn('Name: This field is required.',
                      self._invalid_specification({}))

    def test_invalid_cropped_file_suffix(self):
        spec = {'Cropped file suffix' : 'I am not a valid file suffix',}
        res = self._invalid_specification(spec)
        expected = ("Cropped file suffix: Value must be one of ('.bmp', "
                    "'.jpeg', '.jpg', '.png', '.tif', '.tiff').")
        self.assertIn(expected, res)

    def test_unrecognised_cropped_file_suffix(self):
        spec = {'Cropped file suffix' : '.txt',}
        res = self._invalid_specification(spec)
        expected = ("Cropped file suffix: Value must be one of ('.bmp', "
                    "'.jpeg', '.jpg', '.png', '.tif', '.tiff').")
        self.assertIn(expected, res)

    def test_invalid_thumbnail_width(self):
        spec = {'Thumbnail width pixels' : 10,}
        res = self._invalid_specification(spec)
        expected = 'Thumbnail width pixels: Value should be greater than 1024'
        self.assertIn(expected, res)

    def test_no_fields(self):
        self.assertIn('No fields defined.', self._invalid_specification({}))

    def test_illegal_field_name(self):
        res = self._invalid_specification({'Fields': [{'Name': 'ItemNumber'}]})
        self.assertIn("ItemNumber: Name: 'Name' should not be one of ['ItemNumber'].", res)

    @unittest.skip('Check not implemented')
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

    @unittest.skip('Check not implemented')
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
        expected = 'F: Choices: One or more values must be given.'
        self.assertIn(expected, res)

    def test_duplicated_choices(self):
        "Choices contains duplicated values"
        spec = {'Fields': [
            {'Name': 'F', 'Choices': ['A', 'A']},
        ]}
        res = self._invalid_specification(spec)
        expected = 'F: Choices: Values must be unique.'
        self.assertIn(expected, res)

    def test_empty_choices(self):
        spec = {'Fields': [
            {'Name': 'F', 'Choices': []},
        ]}
        res = self._invalid_specification(spec)
        expected = 'F: Choices: One or more values must be given.'
        self.assertIn(expected, res)

    @unittest.skip('Check not implemented')
    def test_empty_choices_with_data(self):
        spec = {'Fields': [
            {'Name': 'F', 'Choices with data': {}},
        ]}
        res = self._invalid_specification(spec)
        expected = 'Empty "Choices with data" for [F]'
        self.assertIn(expected, res)

    @unittest.skip('Check not implemented')
    def test_choices_with_data_clash(self):
        "A field name clashes with a 'Choices with data' value field"
        spec = {'Fields': [
            {'Name': 'F2-value'},
            {'Name': 'F2', 'Choices with data': {}},
        ]}
        res = self._invalid_specification(spec)
        expected = 'A field named "F2-value" cannot be defined'
        self.assertIn(expected, res)

    def test_empty_parser(self):
        spec = {'Fields': [
            {'Name': 'F1', 'Parser': ''},
        ]}
        res = self._invalid_specification(spec)
        expected = ("F1: Parser: Value must be one of ['date', 'float', "
                    "'float_ge0', 'float_gt0', 'four_digit_int', 'int', "
                    "'int_ge0', 'int_gt0', 'latitude', 'longitude', "
                    "'one_or_two_digit_int', 'sparse_date'].")
        self.assertIn(expected, res)

    def test_unrecognised_parser(self):
        spec = {'Fields': [
            {'Name': 'F1', 'Parser': 'Not a parser'},
        ]}
        res = self._invalid_specification(spec)
        expected = ("F1: Parser: Value must be one of ['date', 'float', "
            "'float_ge0', 'float_gt0', 'four_digit_int', 'int', 'int_ge0', "
            "'int_gt0', 'latitude', 'longitude', 'one_or_two_digit_int', "
            "'sparse_date'].")
        self.assertIn(expected, res)

    def test_parser_and_parserregex(self):
        spec = {'Fields': [
            {'Name': 'F1', 'Parser': 'int', "Regex parser": '[0-9]+'},
        ]}
        res = self._invalid_specification(spec)
        expected = "F1: Parser: 'Parser' and 'Regex parser' are mutually exclusive."
        self.assertIn(expected, res)

    def test_user_template_two_validation_errors(self):
        with self.assertRaises(InvalidSpecificationError) as cm:
            user_template_from_specification({})

        self.assertEqual('2 problems:\nName: This field is required.\nNo fields defined.',
                         str(cm.exception))
        self.assertEqual(['Name: This field is required.', 'No fields defined.'],
                         cm.exception.problems)

    def test_user_template_one_validation_error(self):
        with self.assertRaises(InvalidSpecificationError) as cm:
            user_template_from_specification({'Name': 'T1'})

        self.assertEqual('1 problem:\nNo fields defined.', str(cm.exception))
        self.assertEqual(['No fields defined.'], cm.exception.problems)


if __name__=='__main__':
    unittest.main()
