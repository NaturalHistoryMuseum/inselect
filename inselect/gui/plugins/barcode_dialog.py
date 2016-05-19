from PySide.QtGui import (QDialog, QRadioButton, QVBoxLayout, QLabel, QWidget,
                          QDialogButtonBox, QFrame)

from inselect.lib.utils import debug_print
from inselect.gui.utils import HTML_LINK_TEMPLATE

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
    STYLESHEET = """
    QWidget {
        margin-left: 30px;
    }
    """

    def __init__(self, parent=None):
        super(BarcodeDialog, self).__init__(parent)

        settings = current_settings()

        self._layout = QVBoxLayout()
        prompt = QLabel(
            'The "Read barcodes" command will set each box\'s "Catalog number" '
            'metadata field with value(s) of any barcodes.\n'
            '\n'
            'Use the controls below to indicate how barcodes should be read. '
            'Some options might be unavailable.')
        prompt.setWordWrap(True)
        self._layout.addWidget(prompt)
        self._layout.addWidget(HorizontalLine())

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
        radio = QRadioButton(
            'My objects are labelled with either 1D barcodes or QR codes')
        radio.setChecked('zbar' == settings['engine'])
        radio.setEnabled(zbar_available())
        self._layout.addWidget(radio)

        prompt = QLabel(HTML_LINK_TEMPLATE.format(
            'Barcodes will be decoded using the open-source '
            '<a href="http://zbar.sourceforge.net/">ZBar</a> library'
        ))
        prompt.setOpenExternalLinks(True)
        prompt.setStyleSheet(self.STYLESHEET)
        self._layout.addWidget(prompt)

        self._layout.addWidget(HorizontalLine())
        return radio

    def _create_libdmtx(self, settings):
        radio = QRadioButton('My objects are labelled with Data Matrix barcodes')
        radio.setChecked('libdmtx' == settings['engine'])
        radio.setEnabled(libdmtx_available())
        self._layout.addWidget(radio)

        prompt = QLabel(HTML_LINK_TEMPLATE.format(
            'Barcodes will be decoded using the open-source '
            '<a href="http://www.libdmtx.org/">libdmtx</a> library'
        ))
        prompt.setOpenExternalLinks(True)
        prompt.setStyleSheet(self.STYLESHEET)
        self._layout.addWidget(prompt)

        self._layout.addWidget(HorizontalLine())
        return radio

    def _create_inlite(self, settings):
        radio = QRadioButton(
            'Either my objects are labelled with a barcode not listed above '
            'or I would like the performance and reliability of a commercial '
            'library')
        radio.setChecked('inlite' == settings['engine'])
        radio.setEnabled(inlite_available())
        self._layout.addWidget(radio)

        prompt = QLabel(HTML_LINK_TEMPLATE.format(
            'Only available on Windows. '
            'Visit <a href="http://www.inliteresearch.com/">Inlite Research</a> '
            'to download and install Inlite Research\'s ClearImage library.'
        ))
        prompt.setWordWrap(True)
        prompt.setOpenExternalLinks(True)
        prompt.setStyleSheet(self.STYLESHEET)
        self._layout.addWidget(prompt)

        prompt = QLabel('My objects are labelled with:')
        format = settings['inlite-format']
        radio_1d = QRadioButton('1D barcodes')
        radio_1d.setChecked('1d' == format)
        radio_datamatrix = QRadioButton('Data Matrix barcodes')
        radio_datamatrix.setChecked('datamatrix' == format)
        radio_pdf417 = QRadioButton('PDF 417 barcodes')
        radio_pdf417.setChecked('pdf417' == format)
        radio_qr = QRadioButton('QR codes')
        radio_qr.setChecked('qrcode' == format)

        layout = QVBoxLayout()
        layout.addWidget(prompt)
        layout.addWidget(radio_1d)
        layout.addWidget(radio_datamatrix)
        layout.addWidget(radio_pdf417)
        layout.addWidget(radio_qr)

        group = QWidget()
        group.setLayout(layout)
        group.setStyleSheet(self.STYLESHEET)
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
        self._radio_inlite.toggled.disconnect()

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
