import humanize
import locale
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QFormLayout, QLabel, QWidget

from inselect.lib.utils import format_dt_display
from inselect.gui.utils import BoldLabel, HorizontalLine, reveal_path

from .popup_panel import PopupPanel
from .utils import report_to_user


class RevealPathLabel(QLabel):
    """A QLabel that, when clicked, reveals a path in Finder / Explorer
    """
    def __init__(self, parent=None, flags=Qt.WindowFlags(0)):
        super(RevealPathLabel, self).__init__('', parent, flags)
        self.path = None
        self.setCursor(Qt.PointingHandCursor)

    def set_label_and_path(self, path):
        if path:
            self.setText(path.name)
            self.path = path
        else:
            self.setText('')
            self.path = None

    @report_to_user
    def mouseReleaseEvent(self, event):
        """QLabel virtual
        """
        if self.path:
            reveal_path(self.path)


class InfoWidget(PopupPanel):
    """Shows information about the document and the scanned image
    """
    def __init__(self, parent=None):
        layout = QFormLayout()

        self._document_path = RevealPathLabel()
        layout.addRow('Name', self._document_path)

        self._created_by = QLabel()
        layout.addRow('Created by', self._created_by)

        self._created_on = QLabel()
        layout.addRow('Created on', self._created_on)

        self._last_saved_by = QLabel()
        layout.addRow('Last saved by', self._last_saved_by)

        self._last_saved_on = QLabel()
        layout.addRow('Last saved on', self._last_saved_on)

        layout.addRow(HorizontalLine())

        layout.addRow(BoldLabel('Original full-resolution image'))
        self._scanned_path = RevealPathLabel()
        layout.addRow('File', self._scanned_path)

        self._scanned_size = QLabel()
        layout.addRow('File size', self._scanned_size)

        self._scanned_dimensions = QLabel()
        layout.addRow('Dimensions', self._scanned_dimensions)

        layout.addRow(HorizontalLine())
        layout.addRow(BoldLabel('Thumbnail image'))
        self._thumbnail_path = RevealPathLabel()
        layout.addRow('File', self._thumbnail_path)

        self._thumbnail_size = QLabel()
        layout.addRow('File size', self._thumbnail_size)

        self._thumbnail_dimensions = QLabel()
        layout.addRow('Dimensions', self._thumbnail_dimensions)

        labels_widget = QWidget()
        labels_widget.setLayout(layout)

        # Widget containing toggle label and container
        super(InfoWidget, self).__init__(
            'Information', labels_widget, initially_visible=False, parent=parent
        )

    def _update_file_controls(self, img, path, size, dimensions):
        dim = '{0} x {1}'
        if img.available:
            path.set_label_and_path(img.path)
            size.setText(humanize.naturalsize(img.size_bytes, binary=True))
            dimensions.setText(dim.format(*(
                locale.format("%d", n, grouping=True)
                for n in img.dimensions)
            ))
        else:
            path.setText('')
            size.setText('')
            dimensions.setText('')

    def set_document(self, document):
        """Updates controls to reflect the document. Clears controls if
        document is None.
        """
        if document:
            self._document_path.set_label_and_path(document.document_path)

            p = document.properties
            self._created_by.setText(p.get('Created by'))

            dt = p.get('Created on')
            self._created_on.setText(format_dt_display(dt) if dt else '')

            self._last_saved_by.setText(p.get('Saved by'))

            dt = p.get('Saved on')
            self._last_saved_on.setText(format_dt_display(dt) if dt else '')

            self._update_file_controls(
                document.scanned, self._scanned_path, self._scanned_size,
                self._scanned_dimensions
            )

            self._update_file_controls(
                document.thumbnail, self._thumbnail_path, self._thumbnail_size,
                self._thumbnail_dimensions
            )
        else:
            self._document_path.setText('')
            self._created_by.setText('')
            self._created_on.setText('')
            self._last_saved_by.setText('')
            self._last_saved_on.setText('')
            self._scanned_path.setText('')
            self._scanned_size.setText('')
            self._scanned_dimensions.setText('')
            self._thumbnail_path.setText('')
            self._thumbnail_size.setText('')
            self._thumbnail_dimensions.setText('')
