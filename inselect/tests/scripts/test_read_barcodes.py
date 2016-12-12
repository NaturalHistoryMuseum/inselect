import unittest

from pathlib import Path

from inselect.lib.document import InselectDocument

from inselect.scripts.read_barcodes import main

from inselect.tests.utils import temp_directory_with_files

try:
    from gouda.engines.libdmtx import LibDMTXEngine
except ImportError:
    LibDMTXEngine = None


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestReadBarcodes(unittest.TestCase):
    @unittest.skipIf(LibDMTXEngine is None or not LibDMTXEngine.available(),
                     "LibDMTXEngine not available")
    def test_read_barcodes(self):
        "Read barcodes"
        with temp_directory_with_files(TESTDATA / 'barcodes.inselect',
                                       TESTDATA / 'barcodes.jpg') as tempdir:
            doc_path = tempdir.joinpath('barcodes.inselect')

            # Doc should not have any catalog numbers
            doc = InselectDocument.load(doc_path)
            self.assertFalse(
                any(v.get('fields', {}).get('catalogNumber') for v in doc.items)
            )

            main([str(tempdir), 'libdmtx'])

            # Doc should not have expected catalog numbers
            doc = InselectDocument.load(doc_path)
            self.assertEqual(
                ['1681107', '1681110', '1681112'],
                sorted(v['fields']['catalogNumber'] for v in doc.items)
            )


if __name__ == '__main__':
    unittest.main()
