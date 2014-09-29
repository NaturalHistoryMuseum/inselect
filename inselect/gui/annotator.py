from PySide import QtCore, QtGui
import inselect.settings

DIALOG_PARENT_RATIO = 0.75
DIALOG_HEADER_HEIGHT = 50
SIDEBAR_MIN_WIDTH = 200
IMAGE_DIALOG_WIDTH_RATIO = 0.5
IMAGE_DIALOG_HEIGHT_RATIO = 0.9


class AnnotateDialog(QtGui.QDialog):
    """ Dialog that handles annotation of a segment. """
    def __init__(self, graphics_scene, segments, parent=None):
        # Constructors
        super(AnnotateDialog, self).__init__(parent)
        # Setup members
        self._fields = inselect.settings.get('annotation_fields')
        self._graphics_scene = graphics_scene
        self._segment_scene = self._graphics_scene.segment_scene()
        self._parent = parent
        self._image = None
        self._table = None
        if isinstance(segments, list):
            self._segments = list(segments)
        else:
            self._segments = [segments]
        self._single_segment = len(self._segments) == 1
        self._sidebar_width = SIDEBAR_MIN_WIDTH
        # Setup UI
        self.setWindowTitle('Annotate Segment')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        # Call place_dialog early as we want to know width/height for layout.
        self._place_dialog()
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
        self._help_text.setFixedWidth(self._sidebar_width)
        self._help_text.setWordWrap(True)
        self._warning_text = QtGui.QLabel("""
           <p><span style="font-size: 10pt; color: #F00">Warning: You are
           editing more than one segment. Only values shared by all segments
           are displayed here.</span></p>
        """)
        self._warning_text.setFixedWidth(self._sidebar_width)
        self._warning_text.setWordWrap(True)
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
            self._layout.addWidget(self._warning_text, 1, 0,
                                   QtCore.Qt.AlignTop)
            self._layout.addWidget(self._help_text, 2, 0,
                                   QtCore.Qt.AlignBottom)
            self._layout.addWidget(self._table, 1, 1, 2, 1)
        self._layout.addWidget(self._button_box, 3, 0, 1, 2)
        self.setLayout(self._layout)

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

    def _place_dialog(self):
        """Place/size the dialog on the screen

        This will initialize the dialog and sidebar's width, so should be
        called early.
        """
        self.resize(max(500, int(DIALOG_PARENT_RATIO * self._parent.width())),
                    max(500, int(DIALOG_PARENT_RATIO * self._parent.height())))
        screen_rect = self._parent.app.desktop().availableGeometry()
        self.move(screen_rect.center() - self.rect().center())
        if self._single_segment:
            self._sidebar_width = self.width() * IMAGE_DIALOG_WIDTH_RATIO


    def _setup_image(self):
        """Setup and populate the label for this segment

        If the label does not exist, create it - otherwise use the existing
        label. This means this can be used to refresh the label when updating
        the segment
        """
        if self._image is None:
            self._image = QtGui.QLabel(self)
        if self._single_segment:
            pixmap = self._graphics_scene.get_segment_pixmap(
                self._segments[0], self._sidebar_width,
                self.height() * IMAGE_DIALOG_HEIGHT_RATIO,
                border=False, padding=False
            )
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
        if self._single_segment:
            segment_values = self._segments[0].fields()
        else:
            segment_values = self._segments[0].fields()
            for i in range(1, len(self._segments)):
                new_values = self._segments[i].fields()
                for field, value in new_values.items():
                    if field not in segment_values:
                        segment_values[field] = ''
                    elif segment_values[field] != value:
                        segment_values[field] = ''
        for row, field in enumerate(self._fields):
            if field in segment_values:
                value = segment_values[field]
            else:
                value = ''
            item = QtGui.QTableWidgetItem()
            item.setData(QtCore.Qt.EditRole, value)
            self._table.setItem(row, 0, item)

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
        next_segment = self._segment_scene.get_next_segment(self._segments[0])
        self._graphics_scene.select_segment(next_segment)
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
        p_segment = self._segment_scene.get_previous_segment(self._segments[0])
        self._graphics_scene.select_segment(p_segment)
        self._segments = [p_segment]
        self._setup_table()
        self._setup_image()
        self._table.setFocus()