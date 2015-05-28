from PySide.QtCore import Qt
from PySide.QtGui import (QDialog, QRadioButton, QVBoxLayout, QLabel, QWidget,
                          QDialogButtonBox, QFrame)

from inselect.lib.utils import debug_print

from .barcode_settings import (current_settings, update_settings,
                               inlite_available, libdmtx_available,
                               zbar_available)


class HorizontalLine(QFrame):
    """A horizontal line
    """
    def __init__(self, parent=None):
        super(HorizontalLine, self).__init__(parent)
        self.setFrameShape(QFrame.HLine)


class BarcodeDialog(QDialog):
    def __init__(self, parent=None):
        super(BarcodeDialog, self).__init__(parent)

        settings = current_settings()

        self._layout = QVBoxLayout()
        self._radio_libdmtx = self._create_libdmtx(settings)
        self._radio_zbar = self._create_zbar(settings)
        (self._radio_inlite, self._inlite_1d, self._inlite_datamatrix,
         self._inlite_pdf417, self._inlite_qr) = self._create_inlite(settings)

        self._buttons = QDialogButtonBox(QDialogButtonBox.Ok |
                                         QDialogButtonBox.Cancel)

        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        self._layout.addWidget(self._buttons)
        self.setLayout(self._layout)

        self.setWindowTitle('Read barcodes')

    def _create_zbar(self, settings):
        radio = QRadioButton('The open-source zbar library')
        radio.setChecked('zbar' == settings['engine'])
        radio.setEnabled(zbar_available())
        self._layout.addWidget(radio)

        prompt = QLabel('1D and QR Code barcodes')
        prompt.setEnabled(zbar_available() and 'zbar' == settings['engine'])
        radio.toggled.connect(prompt.setEnabled)
        self._layout.addWidget(prompt)

        self._layout.addWidget(HorizontalLine())
        return radio

    def _create_libdmtx(self, settings):
        radio = QRadioButton('The open-source libdmtx library')
        radio.setChecked('libdmtx' == settings['engine'])
        radio.setEnabled(libdmtx_available())
        self._layout.addWidget(radio)

        prompt = QLabel('DataMatrix barcodes')
        prompt.setEnabled(libdmtx_available() and 'libdmtx' == settings['engine'])
        radio.toggled.connect(prompt.setEnabled)
        self._layout.addWidget(prompt)

        self._layout.addWidget(HorizontalLine())
        return radio

    def _create_inlite(self, settings):
        radio = QRadioButton('The commercial Inlite ClearImage library')
        radio.setChecked('inlite' == settings['engine'])
        radio.setEnabled(inlite_available())
        self._layout.addWidget(radio)

        prompt = QLabel('A wide range of barcodes')

        format = settings['inlite-format']
        radio_1d = QRadioButton('1D')
        radio_1d.setChecked('1d' == format)
        radio_datamatrix = QRadioButton('DataMatrix')
        radio_datamatrix.setChecked('datamatrix' == format)
        radio_pdf417 = QRadioButton('PDF 417')
        radio_pdf417.setChecked('pdf417' == format)
        radio_qr = QRadioButton('QR Codes')
        radio_qr.setChecked('qrcode' == format)

        layout = QVBoxLayout()
        layout.addWidget(prompt)
        layout.addWidget(radio_1d)
        layout.addWidget(radio_datamatrix)
        layout.addWidget(radio_pdf417)
        layout.addWidget(radio_qr)

        prompt = QLabel('A wide range of barcodes')

        group = QWidget()
        group.setLayout(layout)
        radio.toggled.connect(group.setEnabled)
        group.setEnabled(inlite_available() and 'inlite' == settings['engine'])

        self._layout.addWidget(group)

        return radio, radio_1d, radio_datamatrix, radio_pdf417, radio_qr

    def done(self, r):
        """QDialog virtual
        """
        debug_print('BarcodeDialog.done', r)

        # Necessary to avoid core dump on process exit
        self._buttons.accepted.disconnect()
        self._buttons.rejected.disconnect()

        super(BarcodeDialog, self).done(r)

    def accept(self):
        """QDialog virtual
        """
        debug_print('BarcodeDialog.accept')

        super(BarcodeDialog, self).accept()

        if self._radio_zbar.isChecked():
            engine = 'zbar'
        elif self._radio_libdmtx.isChecked():
            engine = 'libdmtx'
        else:
            engine = 'inlite'

        if self._inlite_1d.isChecked():
            format = '1d'
        elif self._inlite_datamatrix.isChecked():
            format = 'datamatrix'
        elif self._inlite_pdf417.isChecked():
            format = 'pdf417'
        else:
            format = 'qrcode'

        update_settings({'engine': engine, 'inlite-format': format})
