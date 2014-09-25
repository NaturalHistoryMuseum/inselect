from PySide import QtCore, QtGui
import inselect.settings

DIALOG_HEADER_HEIGHT = 50
HELPER_COLUMN_MIN_WIDTH = 200


class AnnotateDialog(QtGui.QDialog):
    """ Dialog that handles annotation of a segment. """
    def __init__(self, segment_scene, segments, parent=None):
        # Constructors
        super(AnnotateDialog, self).__init__(parent)
        # Setup members
        self._fields = inselect.settings.get('annotation_fields')
        self._segment_scene = segment_scene
        self._parent = parent
        self._image = None
        self._table = None
        if isinstance(segments, list):
            self._segments = list(segments)
        else:
            self._segments = [segments]
        self._single_segment = len(self._segments) == 1
        # Setup UI
        self.setWindowTitle('Annotate Segment')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        self._layout = QtGui.QGridLayout(self)
        self._setup_image()
        self._setup_table()
        # Add help text
        self._dialog_header = QtGui.QLabel("""
            <p><span style=" font-size:14pt;">Annotation Editor</span></p>
        """)
        self._dialog_header.setMaximumHeight(DIALOG_HEADER_HEIGHT)
        self._help_text = QtGui.QLabel("""
            <p><span style=" font-size:10pt; font-style:italic;">
                Enter specimen annotation. Cycle through elements with Tab key.
                Go to previous/next specimen with Ctrl+N/Ctrl+P
            </span>.<span style=" font-size:10pt; font-weight:bold;">
                Note that the values are modified directly as you enter them.
             </span></p>
        """)
        self._help_text.setFixedWidth(
            max(inselect.settings.get('icon_size'), HELPER_COLUMN_MIN_WIDTH)
        )
        self._help_text.setWordWrap(True)
        # Add close/prev/next buttons
        self._button_box = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        self._close_button = QtGui.QPushButton('Close')
        self._button_box.addButton(self._close_button,
                                   QtGui.QDialogButtonBox.ActionRole)
        if self._single_segment:
            self._prev_button = QtGui.QPushButton('Previous')
            self._next_button = QtGui.QPushButton('Next')
            self._button_box.addButton(self._prev_button,
                                       QtGui.QDialogButtonBox.ActionRole)
            self._button_box.addButton(self._next_button,
                                       QtGui.QDialogButtonBox.ActionRole)
        # Set layout
        self._layout.addWidget(self._dialog_header, 0, 0, 1, 2)
        if self._single_segment:
            self._layout.addWidget(self._image, 1, 0,
                                   QtCore.Qt.AlignTop)
            self._layout.addWidget(self._help_text, 2, 0,
                                   QtCore.Qt.AlignBottom)
            self._layout.addWidget(self._table, 1, 1, 2, 1)
        else:
            pass
        self._layout.addWidget(self._button_box, 3, 0, 1, 2)
        self.setLayout(self._layout)
        self._place_dialog()

        # Listen to events
        self._table.itemChanged.connect(self._item_changed)
        self._close_button.released.connect(self.reject)
        if self._single_segment:
            self._next_button.released.connect(self._next_segment)
            self._prev_button.released.connect(self._previous_segment)
            # Note we can't use arrows as that used by the field editor.
            self.addAction(QtGui.QAction(
                "Next",
                self,
                shortcut=QtCore.Qt.Key_N+QtCore.Qt.ControlModifier,
                triggered=self._next_segment
            ))
            self.addAction(QtGui.QAction(
                "Previous",
                self,
                shortcut=QtCore.Qt.Key_P+QtCore.Qt.ControlModifier,
                triggered=self._previous_segment
            ))

        # Start with the table focused
        self._table.setFocus()

    def _setup_image(self):
        """Setup and populate the label for this segment

        If the label does not exist, create it - otherwise use the existing
        label. This means this can be used to refresh the label when updating
        the segment
        """
        if self._image is None:
            self._image = QtGui.QLabel(self)
        if self._single_segment:
            icon = self._segment_scene.get_segment_icon(self._segments[0])
            size = inselect.settings.get('icon_size')
            pixmap = icon.pixmap(size, size)
            self._image.setPixmap(pixmap)

    def _setup_table(self):
        """Setup and populate the table for this segment

        If the table does not exist, create it - otherwise use the existing
        label. This means this can be used to refresh the label when updating
        the segment.
        """
        if self._table is None:
            self._table = QtGui.QTableWidget(len(self._fields), 1)
            self._table.setSelectionMode(
                QtGui.QAbstractItemView.SingleSelection
            )
            self._table.setVerticalHeaderLabels(self._fields)
            self._table.horizontalHeader().setStretchLastSection(True)
            self._table.horizontalHeader().hide()
        # Populate the data
        # TODO: If multiple segments share a field's value (eg. taxon name),
        # add it in.
        if self._single_segment:
            segment_values = self._segments[0].fields()
            for row, field in enumerate(self._fields):
                if field in segment_values:
                    value = segment_values[field]
                else:
                    value = ''
                item = QtGui.QTableWidgetItem()
                item.setData(QtCore.Qt.EditRole, value)
                self._table.setItem(row, 0, item)


    def _place_dialog(self):
        """Place/size the dialog on the screen"""
        self.resize(max(500, int(0.66 * self._parent.width())),
                    max(500, int(0.66 * self._parent.height())))
        screen_rect = self._parent.app.desktop().availableGeometry()
        self.move(screen_rect.center() - self.rect().center())

    def _item_changed(self, item):
        """Callback invoked when an item is changed

        Parameters
        ----------
        item :
        """
        row = item.row()
        field = self._fields[row]
        for segment in self._segments:
            segment.set_field(field, item.text())

    def _next_segment(self):
        """Update the dialog to present the next segment

        This is invoked when clicking 'next' or using the keyboard shortcut
        """
        if not self._single_segment:
            return
        #TODO: select/deselect box. We need API on graphics_scene for this.
        next_segment = self._segment_scene.get_next_segment(self._segments[0])
        self._segments = [next_segment]
        self._setup_table()
        self._setup_image()
        self._table.setFocus()

    def _previous_segment(self):
        """Update the dialog to present the previous segment

        This is invoked when clicking 'previous' or using the keyboard shortcut
        """
        if not self._single_segment:
            return
        #TODO: select/deselect box. We need API on graphics_scene for this.
        p_segment = self._segment_scene.get_previous_segment(self._segments[0])
        self._segments = [p_segment]
        self._setup_table()
        self._setup_image()
        self._table.setFocus()