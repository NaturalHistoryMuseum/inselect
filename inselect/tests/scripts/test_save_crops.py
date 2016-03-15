import unittest
import sys

from pathlib import Path

from inselect.scripts.save_crops import main

from inselect.tests.utils import temp_directory_with_files


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestSaveCrops(unittest.TestCase):
    def test_save_crops_with_existing(self):
        "Attempt to save crops over an existing directory"
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:

            # Create crops dir
            crops = tempdir / 'test_segment_crops'
            crops.mkdir()
            main([unicode(tempdir)])

            # nose hooks up stdout to a file-like object
            stdout = sys.stdout.getvalue()
            self.assertIn('exists - skipping', stdout)

    def test_save_crops(self):
        "Save crops"
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:
            main([unicode(tempdir)])
            crops = tempdir / 'test_segment_crops'
            self.assertEqual(5, len(list(crops.glob('*jpg'))))

    def test_save_crops_with_template(self):
        "Save crops using a metadata template"
        with temp_directory_with_files(TESTDATA / 'test_segment.inselect',
                                       TESTDATA / 'test_segment.png') as tempdir:
            main([unicode(tempdir),
                  u'--template={0}'.format(TESTDATA / 'test.inselect_template')])

            # nose hooks up stdout to a file-like object
            stdout = sys.stdout.getvalue()
            self.assertIn('because there are validation problems', stdout)
            self.assertIn('Box [1] [0001] lacks mandatory field [Taxonomy]', stdout)
            self.assertIn('Box [1] [0001] lacks mandatory field [Location]', stdout)
            self.assertIn(
                'Could not parse value of [catalogNumber] [1] for box [1] [0001]',
                stdout
            )


if __name__ == '__main__':
    unittest.main()
