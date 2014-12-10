import numpy as np
import os
import json
import cv2

from functools import partial
from pathlib import Path

from PySide import QtCore, QtGui
from PySide.QtCore import Qt

import inselect.settings

from inselect.lib import utils
from inselect.lib.document import InselectDocument
from inselect.lib.inselect_error import InselectError
from inselect.lib.segment import segment_grabcut
from inselect.lib.utils import debug_print

from .help_dialog import HelpDialog
from .model import Model
from .progress_dialog import ProgressDialog
from .roles import RotationRole
from .segment_worker_thread import SegmentWorkerThread
from .utils import contiguous, report_to_user
from .views.boxes import BoxesView, GraphicsItemView
from .views.grid import GridView
from .views.metadata import MetadataView
from .views.summary import SummaryView

from inselect.workflow.ingest import ingest_image


class SubSegmentWorkerThread(QtCore.QThread):
    """Sub-segments an existing box
    """
    results = QtCore.Signal(list, np.ndarray)

    def __init__(self, image, box, seed_points, parent=None):
        super(SubSegmentWorkerThread, self).__init__(parent)
        self.image, self.box, self.seed_points = image, window, seed_points

    def run(self):
        rects, display = segment_grabcut(self.image, self.window,
                                         self.seed_points)
        self.results.emit(rects, display)


class MainWindow(QtGui.QMainWindow):
    """The application's main window
    """
    FILE_FILTER = "inselect files (*{0})".format(InselectDocument.EXTENSION)

    def __init__(self, app, filename=None, tabbed=True):
        super(MainWindow, self).__init__()
        self.app = app

        # Boxes view
        self.view_graphics_item = GraphicsItemView()
        # self.boxes_view is a QGraphicsView, not a QAbstractItemView
        self.boxes_view = BoxesView(self.view_graphics_item.scene)

        # Metadata view
        self.view_grid = GridView()
        self.view_metadata = MetadataView()
        metadata = QtGui.QSplitter()
        metadata.addWidget(self.view_grid)
        metadata.addWidget(self.view_metadata.widget)
        metadata.setSizes([450, 50])

        if tabbed:
            # Views in tabs
            self.tabs = QtGui.QTabWidget(self)
            self.tabs.addTab(self.boxes_view, 'Boxes')
            self.tabs.addTab(metadata, 'Metadata')
            self.tabs.setCurrentIndex(1)
        else:
            # Views in a splitter
            self.tabs = QtGui.QSplitter(self)
            self.tabs.addWidget(self.boxes_view)
            self.tabs.addWidget(metadata)
            self.tabs.setSizes([500, 500])

        # Summary view
        self.view_summary = SummaryView()

        # Main window layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.view_summary.widget)
        layout.addWidget(self.tabs)
        box = QtGui.QWidget()
        box.setLayout(layout)
        self.setCentralWidget(box)

        # Document
        self.document = None
        self.document_path = None

        # Model
        self.model = Model()
        self.view_graphics_item.setModel(self.model)
        self.view_grid.setModel(self.model)
        self.view_metadata.setModel(self.model)
        self.view_summary.setModel(self.model)

        # A consistent selection across all views
        sm = self.view_grid.selectionModel()
        self.view_graphics_item.setSelectionModel(sm)
        self.view_metadata.setSelectionModel(sm)
        self.view_summary.setSelectionModel(sm)

        self.padding = 0
        self.segment_display = None
        self.segment_image_visible = False

        self.create_actions()
        self.create_menus()

        # Conect signals
        self.tabs.currentChanged.connect(self.current_tab_changed)
        sm.selectionChanged.connect(self.selection_changed)

        self.worker = self.progress_box = None

        self.empty_document()

        if filename:
            self.open_document(filename)

    @report_to_user
    def new_document(self):
        """Creates a new document. The user is prompted for the path to a
        scanned image, for which the document will be created.
        """
        debug_print('MainWindow.new_document')

        if not self.close_document():
            # User does not want to close the existing document
            pass
        else:
            # Source image
            folder = inselect.settings.get("working_directory")
            source, selected_filter = QtGui.QFileDialog.getOpenFileName(
                    self, "Choose image for the new inselect document", folder,
                    filter='Images (*.tiff *.png *.jpeg *.jpg)')

            if source:
                source = Path(source)
                doc = ingest_image(source, source.parent)
                self.open_document(doc.document_path)
                msg = 'New inselect document [{0}] created in [{1}]'
                msg = msg.format(doc.document_path.stem, doc.document_path.parent)
                QtGui.QMessageBox.information(self, "Document created", msg)

    @report_to_user
    def open_document(self, filename=None):
        """Opens filename. If filename does not evaluate to True, the user is
        prompted for a filename.
        """
        debug_print('MainWindow.open_document', '[{0}]'.format(str(filename)))

        if not filename:
            folder = inselect.settings.get("working_directory")
            filename, _ = QtGui.QFileDialog.getOpenFileName(
                self, "Open", folder, self.FILE_FILTER)

        if filename:
            filename = Path(filename)
            document = InselectDocument.load(filename)
            inselect.settings.set_value('working_directory', str(filename.parent))

            self.document = document
            self.document_path = filename
            self.model.from_document(self.document)

            # TODO LH Prefer setWindowFilePath to setWindowTitle?
            self.setWindowTitle(u"inselect [{0}]".format(self.document_path.stem))

            self.sync_ui()

    @report_to_user
    def save_document(self):
        """Saves the document and, if the OKed by the user, writes crops
        """
        debug_print('MainWindow.save_document')
        items = []

        self.model.to_document(self.document)
        self.document.save()
        self.model.clear_modified()

        existing_crops = self.document.crops_dir.is_dir()
        if existing_crops:
            msg = ('The document has been saved.\n\n'
                   'Overwrite the existing cropped specimen images?')
        else:
            msg = ('The document has been saved.\n\n'
                   'Write cropped specimen images?')
        res = QtGui.QMessageBox.question(self, 'Write cropped specimen images?',
            msg, QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)

        if QtGui.QMessageBox.Yes == res:
            self.document.save_crops()

    @report_to_user
    def close_document(self):
        """Closes the document and returns True if not modified or if modified
        and user does not cancel. Does not close the document and returns False
        if modified and users cancels.
        """
        debug_print('MainWindow.close_document')
        if self.model.modified:
            # Ask the user if they work like to save before closing
            res = QtGui.QMessageBox.question(self, 'Save document?',
                'Save the document before closing?',
                (QtGui.QMessageBox.Yes | QtGui.QMessageBox.No |
                 QtGui.QMessageBox.Cancel),
                QtGui.QMessageBox.Yes)

            if QtGui.QMessageBox.Yes == res:
                self.save_document()

            # Answering Yes or No means the document will be closed
            close = QtGui.QMessageBox.Cancel != res
        else:
            # The document is not modified so it is OK to close it
            close = True

        if close:
            self.empty_document()

        return close

    @report_to_user
    def empty_document(self):
        """Creates an empty document
        """
        debug_print('MainWindow.empty_document')
        self.document = None
        self.segment_display = None
        self.segment_image_visible = False
        self.model.clear()

        # TODO LH Prefer setWindowFilePath to setWindowTitle?
        self.setWindowTitle("inselect")

        self.sync_ui()

        # TODO LH Default zoom

    def closeEvent(self, event):
        """QWidget virtual
        """
        debug_print('MainWindow.closeEvent')
        if self.close_document():
            # User wants to close
            event.accept()
        else:
            # User does not want to close
            event.ignore()

    @report_to_user
    def zoom_in(self):
        raise NotImplementedError('MainWindow.zoom_in')
        self.view.zoom(1)

    @report_to_user
    def zoom_out(self):
        raise NotImplementedError('MainWindow.zoom_out')
        self.view.zoom(-1)

    @report_to_user
    def about(self):
        QtGui.QMessageBox.about(
            self,
            inselect.settings.get('about_label'),
            inselect.settings.get('about_text')
        )

    @report_to_user
    def help(self):
        """Open the help dialog"""
        d = HelpDialog(self)
        d.exec_()

    @report_to_user
    def segment_worker_finished(self, rects, display, user_cancelled):
        debug_print('MainWindow.segment_worker_finished')

        worker, self.worker = self.worker, None
        self.progress_box.hide()
        self.progress_box = None
        if user_cancelled:
            QtGui.QMessageBox.information(self, 'Segmentation cancelled',
                'Segmentation was cancelled.\n\nExisting data will not be replaced')
        else:
            # TODO LH Better handling of order of boxes

            # Reverse order so that boxes at the top left are towards the start
            # and boxes at the bottom right are towards the end
            rects = [QtCore.QRect(x, y, w, h) for x, y, w, h in reversed(rects)]
            if self.padding:
                # TODO LH Padding is a fraction of box width or height - better
                # to be a fixed number of pixels?
                p = self.padding
                for i in xrange(0, len(rects)):
                    w, h = rects[i].width(), rects[i].height()
                    rects[i].adjust(-w*p, -h*p, 2*w*p, 2*h*p)

            self.model.set_new_boxes(rects)
            self.segment_display = display.copy()

            if self.segment_image_visible:
                self.display_image(self.segment_display)

            self.sync_ui()

    @report_to_user
    def subsegment_worker_finished(self, rects, display):
        debug_print('MainWindow.subsegment_worker_finished')
        # TODO LH Reinstate

        # Create segmentation image if required
        if self.segment_display is None:
            h, w = self.image_array.shape[:2]
            self.segment_display = np.zeros((h, w, 3), dtype=np.uint8)
        x, y, w, h = window
        self.segment_display[y:y+h, x:x+w] = display

        # removes the selected box before replacing it with resegmentations
        self.segment_scene.remove(worker.selected)

        if self.segment_image_visible:
            self.display_image(self.segment_display)

        self.sync_ui()

    @report_to_user
    def segment(self):
        # TODO LH Should be modal
        # TODO LH Allow cancel
        # TODO LH Possible to show progress?

        if self.worker:
            raise InselectError('Reenter segment()')
        else:
            debug_print('MainWindow.segment')
            # Sub-segment a single box if seed points are set, otherwise
            # segment the entire image

            worker = None
            subsegment = False
            if subsegment:
                # TODO LH Reinstate this
                # if object selected, resegment the window
                selected = self.scene.selected_segments()
                if selected:
                    selected = selected[0]
                    window_rect = selected.get_q_rect_f()
                    p = window_rect.topLeft()
                    subsegment_window = [p.x(), p.y(), window_rect.width(),
                                         window_rect.height()]
                    worker = SubSegmentWorkerThread(self.model.image_array,
                        subsegment_window, seed_points)
                    worker.results.connect(self.subsegment_worker_finished)
            else:
                # Segment the entire image
                if self.model.rowCount():
                    prompt = ('Segmenting will cause all boxes and metadata to '
                              'be replaced.\n\nContinue and replace existing '
                              'boxes?')
                    res = QtGui.QMessageBox.question(self, 'Replace existing boxes?',
                        prompt, QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
                if 0 == self.model.rowCount() or QtGui.QMessageBox.Yes == res:
                    worker = SegmentWorkerThread(self.model.image_array,
                                                 self.progress_box)
                    worker.results.connect(self.segment_worker_finished)

            if worker:
                self.progress_box = ProgressDialog(self)
                # Connect the progress box's cancel signal to the worker
                # thread's slot.
                self.progress_box.canceled.connect(worker.user_cancelled)
                self.progress_box.setWindowModality(Qt.WindowModal)
                self.progress_box.setWindowTitle('Segmenting image')
                self.progress_box.setLabelText('Segmenting image')
                self.progress_box.setAutoClose(False)
                self.progress_box.setAutoReset(False)
                self.progress_box.setValue(0)
                self.progress_box.setMaximum(0)
                self.progress_box.setMinimum(0)
                self.progress_box.show()

                self.worker = worker
                self.worker.start()

    @report_to_user
    def select_all(self):
        """Selects all boxes in the model
        """
        sm = self.view_grid.selectionModel()
        m = self.model
        sm.select(QtGui.QItemSelection(m.index(0, 0), m.index(m.rowCount()-1, 0)),
                  QtGui.QItemSelectionModel.Select)

    @report_to_user
    def select_none(self):
        sm = self.view_grid.selectionModel()
        sm.select(QtGui.QItemSelection(), QtGui.QItemSelectionModel.Clear)

    @report_to_user
    def delete(self):
        """Deletes the selected boxes
        """
        # Delete contiguous blocks of rows
        selected = self.view_grid.selectionModel().selectedIndexes()
        selected = sorted([i.row() for i in selected])

        # Remove blocks in reverse order so that row indices are not invalidated
        # TODO LH We shouldn't need to remove blocks in reverse order - stems
        # from crummy GraphicsItemView
        for row, count in reversed(list(contiguous(selected))):
            self.model.removeRows(row, count)

    @report_to_user
    def select_next(self, forwards):
        """The user wants to select the next/previous box
        """
        sm = self.view_grid.selectionModel()
        model = self.view_grid.model()
        current = sm.currentIndex()
        current = current.row() if current else -1

        select = current + (1 if forwards else -1)
        if select == model.rowCount():
            select = 0
        elif -1 == select:
            select = model.rowCount()-1

        debug_print('Will move selection [{0}] from [{1}]'.format(current, select))
        select = model.index(select, 0)
        sm.select(QtGui.QItemSelection(select, select),
                  QtGui.QItemSelectionModel.ClearAndSelect)
        sm.setCurrentIndex(select, QtGui.QItemSelectionModel.Current)

    @report_to_user
    def rotate90(self, clockwise):
        """Rotates the selected boxes 90 either clockwise or counter-clockwise.
        """
        debug_print('MainWindow.rotate')
        value = 90 if clockwise else -90
        selected = self.view_grid.selectionModel().selectedIndexes()
        for index in selected:
            current = index.data(RotationRole)
            self.model.setData(index, current + value, RotationRole)

    @report_to_user
    def display_image(self, image):
        raise NotImplementedError('MainWindow.display_image')

        """Displays an image in the user interface.

        Parameters
        ----------
        image : np.ndarray, QtCore.QImage
            Image to be displayed in viewer.
        """
        if isinstance(image, np.ndarray):
            image = qimage_of_bgr(image)
        self.scene._image_item.setPixmap(QtGui.QPixmap.fromImage(image))

    @report_to_user
    def toggle_padding(self):
        """Action method to toggle box padding."""
        if self.padding == 0:
            self.padding = 0.05
        else:
            self.padding = 0

    @report_to_user
    def toggle_segment_image(self):
        """Action method to switch between display of segmentation image and
        actual image.
        """
        self.segment_image_visible = not self.segment_image_visible
        if self.segment_image_visible:
            image = self.segment_display
        else:
            image = self.qimage
        self.display_image(image)

    def create_actions(self):
        # File menu
        self.new_action = QtGui.QAction("&New...", self,
            shortcut=QtGui.QKeySequence.New, triggered=self.new_document)
        self.open_action = QtGui.QAction("&Open...", self,
            shortcut=QtGui.QKeySequence.Open, triggered=self.open_document,
            icon=self.style().standardIcon(QtGui.QStyle.SP_DialogOpenButton))
        self.save_action = QtGui.QAction("&Save", self,
            shortcut=QtGui.QKeySequence.Save, triggered=self.save_document,
            icon=self.style().standardIcon(QtGui.QStyle.SP_DialogSaveButton))
        self.close_action = QtGui.QAction("&Close", self,
            shortcut=QtGui.QKeySequence.Close, triggered=self.close_document)
        self.exit_action = QtGui.QAction("E&xit", self,
            shortcut=QtGui.QKeySequence.Quit, triggered=self.close)

        # Edit menu
        self.select_all_action = QtGui.QAction("Select &All", self,
            shortcut=QtGui.QKeySequence.SelectAll, triggered=self.select_all)
        # QT does not provide a 'select none' key sequence
        self.select_none_action = QtGui.QAction("Select &None", self,
            shortcut="ctrl+D", triggered=self.select_none)
        self.next_box_action = QtGui.QAction("Next box", self,
            shortcut="N", triggered=partial(self.select_next, forwards=True))
        self.previous_box_action = QtGui.QAction("Previous box", self,
            shortcut="P", triggered=partial(self.select_next, forwards=False))
        # TODO LH Does CMD + Backspace work on a mac?
        self.delete_action = QtGui.QAction("&Delete selected", self,
            shortcut=QtGui.QKeySequence.Delete, triggered=self.delete)
        self.rotate_clockwise_action = QtGui.QAction(
            "Rotate clockwise", self,
            shortcut="R", triggered=partial(self.rotate90, clockwise=True))
        self.rotate_counter_clockwise_action = QtGui.QAction(
            "Rotate counter-clockwise", self, shortcut="L",
            triggered=partial(self.rotate90, clockwise=False))

        # TODO LH Is Refresh (F5) really the right shortcut for the segment
        # action?
        self.segment_action = QtGui.QAction("&Segment", self,
            shortcut="f5", triggered=self.segment,
            icon=self.style().standardIcon(QtGui.QStyle.SP_BrowserReload))
        # LH TODO Fix this action
        self.toggle_padding_action = QtGui.QAction(
            "&Pad boxes", self, shortcut="", enabled=True,
            statusTip="Check to add space around boxes once segmentation has finished",
            checkable=True, triggered=self.toggle_padding)

        # View menu
        self.zoom_in_action = QtGui.QAction("Zoom &In", self,
            shortcut=QtGui.QKeySequence.ZoomIn, triggered=self.zoom_in,
            icon=self.style().standardIcon(QtGui.QStyle.SP_ArrowUp))
        self.zoom_out_action = QtGui.QAction("Zoom &Out", self,
            shortcut=QtGui.QKeySequence.ZoomOut, triggered=self.zoom_out,
            icon=self.style().standardIcon(QtGui.QStyle.SP_ArrowDown))

        # TODO LH Is F3 (normally meaning 'find next') really the right
        # shortcut for the toggle segment image action?
        self.toggle_segment_action = QtGui.QAction("&Display segmentation", self,
            shortcut="f3", triggered=self.toggle_segment_image,
            statusTip="Display segmentation image", checkable=True)

        # Help menu
        self.about_action = QtGui.QAction("&About", self, triggered=self.about)
        self.help_action = QtGui.QAction("&Help", self,
            shortcut=QtGui.QKeySequence.HelpContents, triggered=self.help)

    def create_menus(self):
        self.toolbar = self.addToolBar("Edit")
        self.toolbar.addAction(self.open_action)
        self.toolbar.addAction(self.save_action)
        self.toolbar.addAction(self.segment_action)
        self.toolbar.addAction(self.zoom_in_action)
        self.toolbar.addAction(self.zoom_out_action)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.new_action)
        self.fileMenu.addAction(self.open_action)
        self.fileMenu.addAction(self.save_action)
        self.fileMenu.addAction(self.close_action)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exit_action)

        self.editMenu = QtGui.QMenu("&Edit", self)
        self.editMenu.addAction(self.select_all_action)
        self.editMenu.addAction(self.select_none_action)
        self.editMenu.addAction(self.delete_action)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.next_box_action)
        self.editMenu.addAction(self.previous_box_action)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.rotate_clockwise_action)
        self.editMenu.addAction(self.rotate_counter_clockwise_action)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.segment_action)
        self.editMenu.addAction(self.toggle_padding_action)

        self.viewMenu = QtGui.QMenu("&View", self)
        self.viewMenu.addAction(self.zoom_in_action)
        self.viewMenu.addAction(self.zoom_out_action)
        self.viewMenu.addAction(self.toggle_segment_action)

        self.helpMenu = QtGui.QMenu("&Help", self)
        self.helpMenu.addAction(self.help_action)
        self.helpMenu.addAction(self.about_action)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.editMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def current_tab_changed(self, index):
        """Slot for self.tabs.currentChanged() signal
        """
        self.sync_ui()

    def selection_changed(self, selected, deselected):
        """Slot for self.grid_view.selectionModel().selectionChanged() signal
        """
        self.sync_ui()

    def sync_ui(self):
        """Synchronise the user interface with the application state
        """
        document = self.document is not None
        has_rows = self.model.rowCount()>0 if self.model else False
        boxes_view_visible = self.boxes_view == self.tabs.currentWidget()
        has_selection = len(self.view_grid.selectionModel().selectedIndexes())>0

        # File
        self.save_action.setEnabled(document)
        self.close_action.setEnabled(document)

        # Edit
        self.select_all_action.setEnabled(has_rows)
        self.select_none_action.setEnabled(document)
        self.delete_action.setEnabled(has_selection)
        self.next_box_action.setEnabled(has_rows)
        self.previous_box_action.setEnabled(has_rows)
        self.rotate_clockwise_action.setEnabled(has_selection)
        self.rotate_counter_clockwise_action.setEnabled(has_selection)
        self.segment_action.setEnabled(document)
        self.toggle_segment_action.setEnabled(self.segment_display is not None)

        # View
        self.zoom_in_action.setEnabled(document and boxes_view_visible)
        self.zoom_out_action.setEnabled(document and boxes_view_visible)
