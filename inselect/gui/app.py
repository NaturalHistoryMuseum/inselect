import numpy as np
import os
import json
import cv2

from functools import wraps
from pathlib import Path

from PySide import QtCore, QtGui

import inselect.settings

from inselect.lib import utils
from inselect.lib.document import InselectDocument
from inselect.lib.inselect_error import InselectError
from inselect.lib.segment import segment_edges, segment_grabcut
from inselect.lib.utils import debug_print

from inselect.gui.model import Model
from inselect.gui.help_dialog import HelpDialog
from inselect.gui.views.boxes import BoxesView, GraphicsItemView
from inselect.gui.views.grid import GridView
from inselect.gui.views.metadata import MetadataView
from inselect.gui.views.summary import SummaryView
from inselect.workflow.ingest import ingest_image

class SegmentWorkerThread(QtCore.QThread):
    """Segments an image
    """
    results = QtCore.Signal(list, np.ndarray)

    def __init__(self, image, parent=None):
        super(SegmentWorkerThread, self).__init__(parent)
        self.image = image

    def run(self):
        rects, display = segment_edges(self.image,
                                       window=None,
                                       resize=(5000, 5000),
                                       variance_threshold=100,
                                       size_filter=1)
        self.results.emit(rects, display)


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


def report_to_user(f):
    """A decorator that reports exceptions to the user
    """
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        try:
            return f(self, *args, **kwargs)
        except Exception as e:
            QtGui.QMessageBox.critical(self, u'An error occurred',
                u'An error occurred:\n{0}'.format(e))
            raise
    return wrapper


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

        self.view_graphics_item.setSelectionModel(self.view_grid.selectionModel())
        self.view_metadata.setSelectionModel(self.view_grid.selectionModel())
        self.view_summary.setSelectionModel(self.view_grid.selectionModel())

        self.padding = 0
        self.segment_display = None
        self.segment_image_visible = False

        self.create_actions()
        self.create_menus()

        self.worker = self.progressDialog = None

        self.empty_document()

        if filename:
            self.open_document(filename)

        # TODO LH Why is this here and not in create_actions?
        QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Q"), self, self.close)

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
    def segment_worker_finished(self, rects, display):
        debug_print('MainWindow.segment_worker_finished')

        worker, self.worker = self.worker, None
        self.progressDialog.hide()
        self.progressDialog = None

        # add detected boxes
        rects = [QtCore.QRect(x, y, w, h) for x, y, w, h in rects]
        if self.padding:
            # TODO LH Padding is a fraction of box width or height - better
            # to be a fixed number of pixels?
            p = self.padding
            for i in xrange(0, len(rects)):
                w, h = rects[i].width(), rects[i].height()
                rects[i].adjust(-w*p, -h*p, 2*w*p, 2*h*p)

        # TODO LH Order of boxes
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
                              'be replaced.\n\nReplace existing boxes?')
                    res = QtGui.QMessageBox.question(self, 'Replace existing boxes?',
                        prompt, QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
                if 0 == self.model.rowCount() or QtGui.QMessageBox.Yes == res:
                    worker = SegmentWorkerThread(self.model.image_array)
                    worker.results.connect(self.segment_worker_finished)

            if worker:
                self.toggle_segment_action.setEnabled(True)
                self.progressDialog = QtGui.QProgressDialog(self)
                self.progressDialog.setWindowTitle("Segmenting...")
                self.progressDialog.setCancelButton(None)
                self.progressDialog.setValue(0)
                self.progressDialog.setMaximum(0)
                self.progressDialog.setMinimum(0)
                self.progressDialog.show()

                self.worker = worker
                self.worker.start()

    @report_to_user
    def select_all(self):
        raise NotImplementedError('MainWindow.select_all')

    @report_to_user
    def select_none(self):
        raise NotImplementedError('MainWindow.select_none')

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
        self.new_action = QtGui.QAction(
            "&New...", self, shortcut="ctrl+N", triggered=self.new_document)
        self.open_action = QtGui.QAction(
            self.style().standardIcon(QtGui.QStyle.SP_DialogOpenButton),
            "&Open...", self, shortcut="ctrl+O", triggered=self.open_document)
        self.save_action = QtGui.QAction(
            self.style().standardIcon(QtGui.QStyle.SP_DialogSaveButton),
            "&Save", self, shortcut="ctrl+s", enabled=False,
            triggered=self.save_document)
        self.close_action = QtGui.QAction(
            "&Close", self, shortcut="ctrl+w", triggered=self.close_document)
        self.exit_action = QtGui.QAction(
            "E&xit", self, shortcut="alt+f4", triggered=self.close)
        # TODO LH Also Ctrl+Q?

        # Edit menu
        self.toggle_padding_action = QtGui.QAction(
            "&Toggle padding", self, shortcut="", enabled=True,
            statusTip="Toggle padding", checkable=True,
            triggered=self.toggle_padding)
        # self.select_all_action = QtGui.QAction(
        #     "Select &All", self, shortcut="ctrl+A", triggered=self.select_all)
        self.select_none_action = QtGui.QAction(
            "Select &None", self, shortcut="ctrl+D", triggered=self.select_none)
        self.segment_action = QtGui.QAction(
            self.style().standardIcon(QtGui.QStyle.SP_BrowserReload),
            "&Segment", self, shortcut="f5", enabled=False,
            statusTip="Segment",
            triggered=self.segment)

        # View menu
        self.zoom_in_action = QtGui.QAction(
            self.style().standardIcon(QtGui.QStyle.SP_ArrowUp),
            "Zoom &In", self, enabled=False, shortcut="Ctrl++",
            triggered=self.zoom_in)
        self.zoom_out_action = QtGui.QAction(
            self.style().standardIcon(QtGui.QStyle.SP_ArrowDown),
            "Zoom &Out", self, enabled=False, shortcut="Ctrl+-",
            triggered=self.zoom_out)
        self.toggle_segment_action = QtGui.QAction(
            "&Display segmentation", self, shortcut="f3", enabled=False,
            statusTip="Display segmentation image", checkable=True,
            triggered=self.toggle_segment_image)

        # Help menu
        self.about_action = QtGui.QAction("&About", self, triggered=self.about)
        self.help_action = QtGui.QAction("&Help", self, triggered=self.help)

    def create_menus(self):
        self.toolbar = self.addToolBar("Edit")
        self.toolbar.addAction(self.open_action)
        self.toolbar.addAction(self.save_action)
        self.toolbar.addAction(self.segment_action)
        self.toolbar.addAction(self.zoom_in_action)
        self.toolbar.addAction(self.zoom_out_action)
        self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.fileMenu = QtGui.QMenu("&File", self)
        self.fileMenu.addAction(self.new_action)
        self.fileMenu.addAction(self.open_action)
        self.fileMenu.addAction(self.save_action)
        self.fileMenu.addAction(self.close_action)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exit_action)

        self.editMenu = QtGui.QMenu("&Edit", self)
        self.editMenu.addAction(self.toggle_padding_action)
        # self.editMenu.addAction(self.select_all_action)
        self.editMenu.addAction(self.select_none_action)
        self.fileMenu.addSeparator()
        self.editMenu.addAction(self.segment_action)

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

    def sync_ui(self):
        """Synchronise the user interface with the application state
        """
        if self.document:
            self.toggle_segment_action.setEnabled(self.segment_display is not None)
            self.segment_action.setEnabled(True)
            self.zoom_in_action.setEnabled(True)
            self.zoom_out_action.setEnabled(True)
            self.save_action.setEnabled(True)
            self.close_action.setEnabled(True)
        else:
            self.toggle_segment_action.setEnabled(False)
            self.segment_action.setEnabled(False)
            self.zoom_in_action.setEnabled(False)
            self.zoom_out_action.setEnabled(False)
            self.save_action.setEnabled(False)
            self.close_action.setEnabled(False)
