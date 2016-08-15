import unittest
import shutil

from functools import partial
from mock import patch
from pathlib import Path

from PySide.QtGui import QMessageBox

from inselect.gui.plugins import barcode_settings
from inselect.gui.roles import MetadataRole
from inselect.tests.utils import temp_directory_with_files

from .gui_test import GUITest


try:
    from gouda.engines.libdmtx import LibDMTXEngine
except ImportError:
    LibDMTXEngine = None


TESTDATA = Path(__file__).parent.parent / 'test_data'


class TestReadBarcodes(GUITest):
    @unittest.skipIf(LibDMTXEngine is None or not LibDMTXEngine.available(),
                     "LibDMTXEngine not available")
    @patch.object(QMessageBox, 'warning', return_value=QMessageBox.Ok)
    @patch.object(barcode_settings, 'current_settings',
                  return_value={'engine': 'libdmtx'})
    def test_read_barcodes(self, current_settings, mock_warning):
        self.window.open_document(TESTDATA / 'barcodes.inselect')

        model = self.window.model
        self.assertFalse(model.is_modified)

        self.run_async_operation(partial(self.window.run_plugin, 2))

        self.assertTrue(model.is_modified)

        # User should not have been warned about missing scanned image
        self.assertFalse(mock_warning.called)

        indexes = [model.index(row, 0) for row in range(3)]
        self.assertEqual(
            ['1681107', '1681110', '1681112'],
            sorted(model.data(i, MetadataRole).get('catalogNumber') for i in indexes)
        )

        # Clean up by closing the document
        with patch.object(QMessageBox, 'question', return_value=QMessageBox.No):
            self.assertTrue(self.window.close_document())

    @unittest.skipIf(LibDMTXEngine is None or not LibDMTXEngine.available(),
                     "LibDMTXEngine not available")
    @patch.object(QMessageBox, 'warning', return_value=QMessageBox.Ok)
    def test_read_barcodes_no_scanned_image(self, mock_warning):
        """The user is informed that barcodes cxannot be read without the
        scanned image
        """
        with temp_directory_with_files(TESTDATA / 'barcodes.inselect') as tempdir:
            # Create thumbnail file
            shutil.copy(str(TESTDATA.joinpath('barcodes.jpg')),
                        str(tempdir.joinpath('barcodes_thumbnail.jpg')))
            self.window.open_document(tempdir / 'barcodes.inselect')

            self.window.run_plugin(2)

            expected = ('Unable to read barcodes because the original '
                        'full-resolution image file does not exist.')
            self.assertTrue(expected in mock_warning.call_args[0])

            model = self.window.model

            # Metadata should be unaltered
            indexes = (model.index(row, 0) for row in range(3))
            self.assertEqual(
                [None, None, None],
                [model.data(i, MetadataRole).get('catalogNumber') for i in indexes]
            )

            self.assertFalse(model.is_modified)


if __name__ == '__main__':
    unittest.main()
