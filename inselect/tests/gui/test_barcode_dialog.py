import unittest

from mock import patch
from pathlib import Path

from PySide.QtCore import QSettings

from inselect.gui.plugins.barcode_dialog import BarcodeDialog

from gui_test import MainWindowTest


class TestBarcodeDialog(MainWindowTest):
    """Tests the config dialog box of the 'Read barcode' plugin
    """
    @patch.object(QSettings, 'setValue')
    @patch.object(QSettings, 'value')
    def test_dialog_options_not_changed(self, mock_value, mock_setValue):
        "User does not alter options"
        side_effect = {'barcode/engine': 'libdmtx',
                       'barcode/inlite-format': 'qrcode'}.get
        mock_value.side_effect = side_effect
        dlg = BarcodeDialog()
        dlg.accept()

        mock_setValue.assert_any_call('barcode/engine', 'libdmtx')
        mock_setValue.assert_any_call('barcode/inlite-format', 'qrcode')

    @patch.object(QSettings, 'setValue')
    @patch.object(QSettings, 'value')
    def test_dialog_options_altered_zbar(self, mock_value, mock_setValue):
        "User chooses zbar"
        side_effect = {}.get
        mock_value.side_effect = side_effect
        dlg = BarcodeDialog()
        dlg._radio_zbar.setChecked(True)
        dlg.accept()

        mock_setValue.assert_any_call('barcode/engine', 'zbar')

    @patch.object(QSettings, 'setValue')
    @patch.object(QSettings, 'value')
    def test_dialog_options_altered_libdmtx(self, mock_value, mock_setValue):
        "User chooses zbar"
        side_effect = {}.get
        mock_value.side_effect = side_effect
        dlg = BarcodeDialog()
        dlg._radio_libdmtx.setChecked(True)
        dlg.accept()

        mock_setValue.assert_any_call('barcode/engine', 'libdmtx')

    @patch.object(QSettings, 'setValue')
    @patch.object(QSettings, 'value')
    def test_dialog_options_altered_inlite_1d(self, mock_value, mock_setValue):
        "User chooses Inlite 1D"
        side_effect = {}.get
        mock_value.side_effect = side_effect
        dlg = BarcodeDialog()
        dlg._radio_inlite.setChecked(True)
        dlg._inlite_1d.setChecked(True)
        dlg.accept()

        mock_setValue.assert_any_call('barcode/engine', 'inlite')
        mock_setValue.assert_any_call('barcode/inlite-format', '1d')

    @patch.object(QSettings, 'setValue')
    @patch.object(QSettings, 'value')
    def test_dialog_options_altered_inlite_datamatrix(self, mock_value, mock_setValue):
        "User chooses Inlite DataMatrix"
        side_effect = {}.get
        mock_value.side_effect = side_effect
        dlg = BarcodeDialog()
        dlg._radio_inlite.setChecked(True)
        dlg._inlite_datamatrix.setChecked(True)
        dlg.accept()

        mock_setValue.assert_any_call('barcode/engine', 'inlite')
        mock_setValue.assert_any_call('barcode/inlite-format', 'datamatrix')

    @patch.object(QSettings, 'setValue')
    @patch.object(QSettings, 'value')
    def test_dialog_options_altered_inlite_pdf417(self, mock_value, mock_setValue):
        "User chooses Inlite PDF417"
        side_effect = {}.get
        mock_value.side_effect = side_effect
        dlg = BarcodeDialog()
        dlg._radio_inlite.setChecked(True)
        dlg._inlite_pdf417.setChecked(True)
        dlg.accept()

        mock_setValue.assert_any_call('barcode/engine', 'inlite')
        mock_setValue.assert_any_call('barcode/inlite-format', 'pdf417')

    @patch.object(QSettings, 'setValue')
    @patch.object(QSettings, 'value')
    def test_dialog_options_altered_inlite_qrcode(self, mock_value, mock_setValue):
        "User chooses Inlite QR Code"
        side_effect = {}.get
        mock_value.side_effect = side_effect
        dlg = BarcodeDialog()
        dlg._radio_inlite.setChecked(True)
        dlg._inlite_qr.setChecked(True)
        dlg.accept()

        mock_setValue.assert_any_call('barcode/engine', 'inlite')
        mock_setValue.assert_any_call('barcode/inlite-format', 'qrcode')

    # TODO LH Test enabled / disabled
    # TODO LH Test load_engine


if __name__=='__main__':
    unittest.main()
