import cv2
import json
import os
import sys

from functools import partial
from itertools import chain, izip
from pathlib import Path

import numpy as np

from PySide import QtCore, QtGui
from PySide.QtCore import Qt, QEvent, QSettings
from PySide.QtGui import (QMenu, QAction, QMessageBox, QIcon, QDesktopServices,
                          QVBoxLayout, QWidget)

import inselect

from inselect.lib import utils
from inselect.lib.document import InselectDocument
from inselect.lib.ingest import ingest_image, IMAGE_PATTERNS, IMAGE_SUFFIXES
from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print

import icons        # Register our icon resources with QT

from .info_widget import InfoWidget
from .metadata_library import metadata_library
from .model import Model
from .plugins.barcode import BarcodePlugin
from .plugins.segment import SegmentPlugin
from .plugins.subsegment import SubsegmentPlugin
from .roles import RotationRole, RectRole
from .utils import contiguous, report_to_user, qimage_of_bgr
from .views.boxes import BoxesView, GraphicsItemView
from .views.metadata import MetadataView
from .views.specimen import SpecimenView
from .views.summary import SummaryView
from .worker_thread import WorkerThread

class MainWindow(QtGui.QMainWindow):
    """The application's main window
    """
    FILE_FILTER = u'Inselect documents (*{0});;Images ({1})'.format(
                           InselectDocument.EXTENSION,
                           u' '.join(IMAGE_PATTERNS))

    def __init__(self, app, filename=None):
        super(MainWindow, self).__init__()
        self.app = app

        # Boxes view
        self.view_graphics_item = GraphicsItemView()
        # self.boxes_view is a QGraphicsView, not a QAbstractItemView
        self.boxes_view = BoxesView(self.view_graphics_item.scene)

        # Specimen, metadata and summary views
        self.view_metadata = MetadataView()
        self.view_specimen = SpecimenView()
        self.view_summary = SummaryView()

        # Views in tabs
        self.tabs = QtGui.QTabWidget()
        self.tabs.addTab(self.boxes_view, 'Boxes')
        self.tabs.addTab(self.view_specimen, 'Specimens')
        self.tabs.setCurrentIndex(0)

        # Information about the loaded document
        self.info_widget = InfoWidget()

        # Metadata view above info
        sidebar_layout = QVBoxLayout()
        sidebar_layout.addWidget(self.view_metadata.widget)
        sidebar_layout.addWidget(self.info_widget)
        sidebar = QWidget()
        sidebar.setLayout(sidebar_layout)

        # Tabs alongside metadata fields
        self.splitter = QtGui.QSplitter()
        self.splitter.addWidget(self.tabs)
        self.splitter.addWidget(sidebar)
        self.splitter.setSizes([600, 300])

        # Main window layout
        self.setCentralWidget(self.splitter)

        # Document
        self.document = None
        self.document_path = None

        # Model
        self.model = Model()
        self.model.modified_changed.connect(self.modified_changed)

        # Views
        self.view_graphics_item.setModel(self.model)
        self.view_metadata.setModel(self.model)
        self.view_specimen.setModel(self.model)
        self.view_summary.setModel(self.model)

        # A consistent selection across all views
        sm = self.view_specimen.selectionModel()
        self.view_graphics_item.setSelectionModel(sm)
        self.view_metadata.setSelectionModel(sm)
        self.view_summary.setSelectionModel(sm)

        # Plugins
        self.plugins = [SegmentPlugin, SubsegmentPlugin, BarcodePlugin]
        self.plugin_actions = len(self.plugins) * [None]    # QActions
        self.plugin_image = None
        self.plugin_image_visible = False

        # Long-running operations are run in their own thread.
        self.running_operation = None

        self.create_actions()
        self.create_menus()

        # Conect signals
        self.tabs.currentChanged.connect(self.current_tab_changed)
        sm.selectionChanged.connect(self.selection_changed)

        # Filter events
        self.tabs.installEventFilter(self)
        self.boxes_view.installEventFilter(self)
        self.view_metadata.installEventFilter(self)
        self.view_specimen.installEventFilter(self)
        self.view_summary.installEventFilter(self)

        self.empty_document()

        self.setAcceptDrops(True)

        if filename:
            self.open_file(filename)

    def modified_changed(self):
        "Updated UI's modified state"
        debug_print('MainWindow.modified_changed')
        self.setWindowModified(self.model.is_modified)

    def eventFilter(self, obj, event):
        "Event filter that accepts drag-drop events"
        if event.type() in (QEvent.DragEnter, QEvent.Drop):
            return True
        else:
            return super(MainWindow, self).eventFilter(obj, event)

    @report_to_user
    def open_file(self, path=None):
        """Opens path, which can be None, the path to an inselect document or
        the path to an image file. If None, the user is prompted to select a
        file.

        * If a .inselect file, the file is opened
        * If an image file for which a .inselect document already exists, the
        .inselect file is opened
        * If a _thumbnail.jpg file corresponding to an existing .inselect file,
        the .inselect file is opened
        * If an image file, a new .inselect file is created and opened
        """
        debug_print(u'MainWindow.open_file [{0}]'.format(path))

        if not path:
            folder = QSettings().value('working_directory',
                QDesktopServices.storageLocation(QDesktopServices.DocumentsLocation))

            path, selectedFilter = QtGui.QFileDialog.getOpenFileName(
                self, "Open", folder, self.FILE_FILTER)

        # path will be None if user cancelled getOpenFileName
        if path:
            path = Path(path)

            # What type of file did the user select?
            document_path = image_path = None
            if InselectDocument.EXTENSION == path.suffix:
                # An inselect document
                document_path = path
            elif path.suffix in IMAGE_SUFFIXES:
                # Compute the path to the inselect document (which may or
                # may not already exist) of the image file
                doc_of_image = path.name.replace(InselectDocument.THUMBNAIL_SUFFIX, u'')
                doc_of_image = path.parent / doc_of_image
                doc_of_image = doc_of_image.with_suffix(InselectDocument.EXTENSION)
                if doc_of_image.is_file():
                    # An image file corresponding to an existing .inselect file
                    document_path = doc_of_image
                else:
                    # An image file
                    image_path = path

            if not self.close_document(document_path):
                # User does not want to close the existing document
                pass
            elif document_path:
                # Open the .inselect document
                debug_print('Opening inselect document [{0}]'.format(document_path))
                self.open_document(document_path)
            elif image_path:
                msg = u'Creating new inselect document for image [{0}]'
                debug_print(msg.format(image_path))
                self.new_document(image_path)
            else:
                raise InselectError('Unknown file type [{0}]'.format(path))

    def new_document(self, path):
        """Creates and opens a new inselect document for the scanned image
        given in path
        """
        debug_print('MainWindow.new_document [{0}]'.format(path))

        path = Path(path)
        if not path.is_file():
            raise InselectError(u'Image file [{0}] does not exist'.format(path))
        else:
            # Callable for worker thread
            class NewDoc(object):
                def __init__(self, image):
                    self.image = image

                def __call__(self, progress):
                    progress('Creating thumbnail of scanned image')
                    doc = ingest_image(self.image, self.image.parent)
                    self.document_path = doc.document_path


            self.run_in_worker(NewDoc(path), 'New document',
                               self.new_document_finished)

    def new_document_finished(self, operation):
        """Called when new_document worker has finished
        """
        debug_print('MainWindow.new_document_finished')

        document_path = operation.document_path
        QSettings().setValue('working_directory', str(document_path.parent))

        self.open_file(document_path)
        msg = u'New Inselect document [{0}] created in [{1}]'
        msg = msg.format(document_path.stem, document_path.parent)
        QMessageBox.information(self, "Document created", msg)

    def open_document(self, path):
        """Opens the inselect document given by path
        """
        debug_print('MainWindow.open_document [{0}]'.format(path))

        path = Path(path)
        document = InselectDocument.load(path)
        QSettings().setValue("working_directory", str(path.parent))

        self.document = document
        self.document_path = path
        self.model.from_document(self.document)

        self.setWindowTitle('')
        self.setWindowFilePath(str(self.document_path))
        self.info_widget.set_document(self.document)

        self.sync_ui()

    @report_to_user
    def save_document(self):
        """Saves the document
        """
        debug_print('MainWindow.save_document')
        items = []

        self.model.to_document(self.document)
        self.document.save()
        self.model.set_modified(False)
        self.info_widget.set_document(self.document)

    @report_to_user
    def save_crops(self):
        """Saves cropped specimen images
        """
        debug_print('MainWindow.save_crops')
        res = QMessageBox.Yes
        existing_crops = self.document.crops_dir.is_dir()

        if existing_crops:
            msg = 'Overwrite the existing cropped specimen images?'
            res = QMessageBox.question(self, 'Write cropped specimen images?',
                msg, QMessageBox.No, QMessageBox.Yes)

        if QMessageBox.Yes == res:
            def save_crops(progress):
                progress('Loading full-resolution scanned image')
                self.document.scanned.array

                progress('Saving crops')
                self.document.save_crops(progress)

            def completed(operation):
                QMessageBox.information(self, "Crops saved", msg)

            self.model.to_document(self.document)
            msg = "{0} crops saved in {1}"
            msg = msg.format(self.document.n_items, self.document.crops_dir)
            self.run_in_worker(save_crops, 'Save crops', completed)

    @report_to_user
    def export_csv(self):
        debug_print('MainWindow.export_csv')

        path = self.document.document_path.with_suffix('.csv')

        res = QMessageBox.Yes
        existing_csv = path.is_file()

        if existing_csv:
            msg = 'Overwrite the existing CSV file?'
            res = QMessageBox.question(self, 'Export CSV file?',
                msg, QMessageBox.No, QMessageBox.Yes)

        if QMessageBox.Yes == res:
            self.model.to_document(self.document)
            self.document.export_csv(path, metadata_library().current)
            msg = "Data for {0} boxes written to {1}"
            msg = msg.format(self.document.n_items, path)
            QMessageBox.information(self, "CSV saved", msg)

    @report_to_user
    def save_screengrab(self):
        """Saves a screenshot to an image file
        """
        debug_print('MainWindow,save_screengrab')

        # Do not use OpenCV to write the image because the conversion from Qt's
        # QPixmap to a numpy array is non-trivial
        # Investigate https://pypi.python.org/pypi/qimage2ndarray/0.2

        # Work out the supported image file extensions
        extensions = QtGui.QImageWriter.supportedImageFormats()
        extensions = sorted([str(e).lower() for e in extensions])
        extensions = ['*.{0}'.format(e) for e in extensions]

        # Only some of these make sense. For example, do not offer the user
        # the change to save an eps, which is a format supported by QImageWriter
        extensions = sorted(set(extensions).intersection(IMAGE_PATTERNS))

        filter = 'Images ({0})'.format(' '.join(extensions))

        # Default folder is the user's documents folder
        folder = QDesktopServices.storageLocation(QDesktopServices.DocumentsLocation)
        path, selected_filter = QtGui.QFileDialog.getSaveFileName(
                self, "Save image file of boxes view", folder,
                filter=filter)

        if path:
            pm = QtGui.QPixmap.grabWidget(self)

            # Write using QImageWriter, which makes richer error information
            # avaible than QPixmap.save()
            writer = QtGui.QImageWriter(path)
            if not writer.write(pm.toImage()):
                msg = 'An error occurred writing to [{0}]: [{1}]'
                raise InselectError(msg.format(path, writer.errorString()))
            else:
                debug_print('BoxesView.save_screengrab [{0}]'.format(path))

    @report_to_user
    def close_document(self, document_to_open=None):
        """Closes the document and returns True if not modified or if modified
        and user does not cancel.

        If document_to_open is given and is the same as self.document_path then
        one of two things will happen. If the model is not modified, the user
        is informed and False is returned. If the model is modified, the user is
        asked if they would like to discard their changes and revert to the
        version on the filesystem. If the user selects No, False is returned.
        If the user selects Yes, the document is closed and True is returned.

        In all cases, if the user selects cancels then the document is not
        closes and False is returned.
        """
        debug_print('MainWindow.close_document', document_to_open)
        # Must make sure that files exist before calling resolve
        if (self.document_path and self.document_path.is_file() and 
            document_to_open and document_to_open.is_file() and
            self.document_path.resolve() == document_to_open.resolve()):
            if self.model.is_modified:
                # Ask the user if they work like to revert
                msg = (u'The document [{0}] is already open and has been '
                       u'changed. Would you like to discard your changes and '
                       u'revert to the previous version?')
                msg = msg.format(self.document_path.stem)
                res = QMessageBox.question(self, u'Discard changes?', msg,
                                           (QMessageBox.Yes | QMessageBox.No),
                                            QMessageBox.No)
                close = QMessageBox.Yes == res
            else:
                # Let the user know that the document is already open and
                # take no action
                msg = u'The document [{0}] is already open'
                msg = msg.format(self.document_path.stem)
                QMessageBox.information(self, 'Document already open', msg,
                                        QMessageBox.Ok)
                close = False
        elif self.model.is_modified:
            # Ask the user if they work like to save before closing
            res = QMessageBox.question(self, 'Save document?',
                'Save the document before closing?',
                (QMessageBox.Yes | QMessageBox.No |
                 QMessageBox.Cancel),
                QMessageBox.Yes)

            if QMessageBox.Yes == res:
                self.save_document()

            # Answering Yes or No means the document will be closed
            close = QMessageBox.Cancel != res
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
        self.document_path = None
        self.plugin_image = None
        self.plugin_image_visible = False
        self.model.clear()

        self.setWindowTitle('Inselect')
        self.setWindowFilePath(None)
        self.info_widget.set_document(None)

        self.sync_ui()

    def closeEvent(self, event):
        """QWidget virtual
        """
        debug_print('MainWindow.closeEvent')
        if self.close_document():
            # User wants to close
            self.write_geometry_settings()
            event.accept()
        else:
            # User does not want to close
            event.ignore()

    @report_to_user
    def zoom_in(self):
        self.boxes_view.zoom_in()

    @report_to_user
    def zoom_out(self):
        self.boxes_view.zoom_out()

    @report_to_user
    def toggle_zoom(self):
        self.boxes_view.toggle_zoom()

    @report_to_user
    def zoom_home(self):
        self.boxes_view.zoom_home()

    @report_to_user
    def show_grid(self):
        self.view_specimen.show_grid()

    @report_to_user
    def show_expanded(self):
        self.view_specimen.show_expanded()

    @report_to_user
    def about(self):
        text = u"""<h1>Inselect {version}</h1>
           <h2>Contributors</h2>
           <p>
               <strong>Alice Heaton</strong>: Application development
           </p>
           <p>
               <strong>Lawrence Hudson</strong>: Application development
           </p>
           <p>
               <strong>Pieter Holtzhausen</strong>: Application development
               and segmentation algorithm
           </p>
           <p>
               <strong>Stefan van der Walt</strong>: Application development
               and segmentation algorithm
           </p>
        """.format(version=inselect.__version__)
        QMessageBox.about(self, 'Inselect', text)

    def run_in_worker(self, operation, name, complete_fn=None):
        """Runs the callable operation in a worker thread. The callable
        complete_fn is called when the operation has finished.
        """
        debug_print("MainWindow.run_in_worker")

        if self.running_operation:
            debug_print('Operation already running')
        else:
            worker = WorkerThread(operation,
                                  name,
                                  self)
            worker.completed.connect(self.worker_finished)

            self.running_operation = (operation, name, complete_fn, worker)
            worker.start()

    @report_to_user
    def worker_finished(self, user_cancelled, error_message):
        debug_print("MainWindow.worker_finished", user_cancelled,
                    error_message)

        operation, name, complete_fn, worker = self.running_operation
        self.running_operation = None

        if user_cancelled:
            QMessageBox.information(self, 'Cancelled',
                                    "'{0} cancelled'".format(name))
        elif error_message:
            QMessageBox.information(self,
                    "An error occurred running '{0}'".format(name),
                    error_message + '\n\nExisting data has not been altered')
        else:
            if complete_fn:
                complete_fn(operation)
            self.sync_ui()

    @report_to_user
    def run_plugin(self, plugin_number):
        """Passes each cropped specimen image through plugin
        """
        debug_print("MainWindow.run_plugin")

        if plugin_number < 0 or plugin_number > len(self.plugins):
            raise ValueError('Unexpected plugin [{0}]'.format(plugin_number))
        else:
            plugin = self.plugins[plugin_number]

            self.model.to_document(self.document)

            # Create the plugin
            operation = plugin(self.document, self)
            if operation.proceed():
                self.run_in_worker(operation,
                                   operation.name(),
                                   self.plugin_finished)
            else:
                pass

    def plugin_finished(self, operation):
        """Called when a plugin has finished running in a worker thread
        """
        debug_print("MainWindow.plugin_finished")

        if hasattr(operation, 'items'):
            self.model.set_new_boxes(operation.items)

        if hasattr(operation, 'display'):
            # An image that can be displayed instead of the main image
            display = operation.display
            self.plugin_image = QtGui.QPixmap.fromImage(qimage_of_bgr(display))
            self.update_boxes_display_pixmap()

    @report_to_user
    def select_all(self):
        """Selects all boxes in the model
        """
        sm = self.view_specimen.selectionModel()
        m = self.model
        sm.select(QtGui.QItemSelection(m.index(0, 0), m.index(m.rowCount()-1, 0)),
                  QtGui.QItemSelectionModel.Select)

    @report_to_user
    def select_none(self):
        sm = self.view_specimen.selectionModel()
        sm.select(QtGui.QItemSelection(), QtGui.QItemSelectionModel.Clear)

    @report_to_user
    def delete_selected(self):
        """Deletes the selected boxes
        """
        # Delete contiguous blocks of rows
        selected = self.view_specimen.selectionModel().selectedIndexes()
        selected = sorted([i.row() for i in selected])

        # Remove blocks in reverse order so that row indices are not invalidated
        # TODO LH We shouldn't need to remove blocks in reverse order - stems
        # from crummy GraphicsItemView
        for row, count in reversed(list(contiguous(selected))):
            self.model.removeRows(row, count)

    @report_to_user
    def select_next_prev(self, next):
        """Selects the next box in the mode if next is True, the previous
        box in the model if next if False.
        """
        sm = self.view_specimen.selectionModel()
        current = sm.currentIndex()
        current = current.row() if current else -1

        select = current + (1 if next else -1)
        if select == self.model.rowCount():
            select = 0
        elif -1 == select:
            select = self.model.rowCount()-1

        debug_print('Will move selection [{0}] from [{1}]'.format(current, select))
        select = self.model.index(select, 0)
        sm.select(QtGui.QItemSelection(select, select),
                  QtGui.QItemSelectionModel.ClearAndSelect)
        sm.setCurrentIndex(select, QtGui.QItemSelectionModel.Current)

    @report_to_user
    def rotate90(self, clockwise):
        """Rotates the selected boxes 90 either clockwise or counter-clockwise.
        """
        debug_print('MainWindow.rotate')
        value = 90 if clockwise else -90
        selected = self.view_specimen.selectionModel().selectedIndexes()
        for index in selected:
            current = index.data(RotationRole)
            self.model.setData(index, current + value, RotationRole)

    def update_boxes_display_pixmap(self):
        """Sets the pixmap in the boxes view
        """
        pixmap = self.plugin_image if self.plugin_image_visible else None
        self.view_graphics_item.show_alternative_pixmap(pixmap)

    @report_to_user
    def toggle_plugin_image(self):
        """Action method to switch between display of the last plugin's 
        information image (if any) and the actual image.
        """
        self.plugin_image_visible = not self.plugin_image_visible
        self.update_boxes_display_pixmap()

    def create_actions(self):
        # File menu
        self.open_action = QAction("&Open...", self,
            shortcut=QtGui.QKeySequence.Open, triggered=self.open_file,
            icon=self.style().standardIcon(QtGui.QStyle.SP_DialogOpenButton))
        self.save_action = QAction("&Save", self,
            shortcut=QtGui.QKeySequence.Save, triggered=self.save_document,
            icon=self.style().standardIcon(QtGui.QStyle.SP_DialogSaveButton))
        self.save_crops_action = QAction("&Save crops", self,
            triggered=self.save_crops)
        self.export_csv_action = QAction("&Export CSV", self,
            triggered=self.export_csv)
        self.save_screengrab_action = QAction("Save screen grab", self,
            triggered=self.save_screengrab)
        self.close_action = QAction("&Close", self,
            shortcut=QtGui.QKeySequence.Close, triggered=self.close_document)
        self.exit_action = QAction("E&xit", self,
            shortcut=QtGui.QKeySequence.Quit, triggered=self.close)

        # Edit menu
        self.select_all_action = QAction("Select &All", self,
            shortcut=QtGui.QKeySequence.SelectAll, triggered=self.select_all)
        # QT does not provide a 'select none' key sequence
        self.select_none_action = QAction("Select &None", self,
            shortcut="ctrl+D", triggered=self.select_none)
        self.next_box_action = QAction("Next box", self,
            shortcut="ctrl+N", triggered=partial(self.select_next_prev, next=True))
        self.previous_box_action = QAction("Previous box", self,
            shortcut="ctrl+P", triggered=partial(self.select_next_prev, next=False))

        # TODO LH Does CMD + Backspace work on a mac?
        self.delete_action = QAction("&Delete selected", self,
            shortcut=QtGui.QKeySequence.Delete, triggered=self.delete_selected)
        self.rotate_clockwise_action = QAction(
            "Rotate clockwise", self,
            shortcut="R", triggered=partial(self.rotate90, clockwise=True))
        self.rotate_counter_clockwise_action = QAction(
            "Rotate counter-clockwise", self, shortcut="L",
            triggered=partial(self.rotate90, clockwise=False))

        # Plugins
        # Plugin shortcuts start at F5
        shortcut_offset = 5
        for index, plugin in enumerate(self.plugins):
            action = QAction(plugin.name(), self,
                             triggered=partial(self.run_plugin, index))
            shortcut_fkey = index + shortcut_offset
            if shortcut_fkey < 13:
                # Keyboards typically have 12 function keys
                action.setShortcut('f{0}'.format(shortcut_fkey))
            icon = plugin.icon()
            if icon:
                action.setIcon(icon)
            self.plugin_actions[index] = action

        # View menu
        # The obvious approach is to set the trigger to
        # partial(self.tabs.setCurrentIndex, 0) but this causes a segfault when
        # the application exits on linux.
        self.boxes_view_action = QAction("&Boxes", self, checkable=True,
            triggered=partial(self.show_tab, 0))
        self.metadata_view_action = QAction("&Specimens", self, checkable=True,
            triggered=partial(self.show_tab, 1))

        # FullScreen added in Qt 5.something
        # https://qt.gitorious.org/qt/qtbase-miniak/commit/1ef8a6d
        if not hasattr(QtGui.QKeySequence, 'FullScreen'):
            if 'darwin' == sys.platform:
                KeySequenceFullScreen = 'shift+ctrl+f'
            else:
                KeySequenceFullScreen = 'f11'
        else:
            KeySequenceFullScreen = QtGui.QKeySequence.FullScreen
        self.full_screen_action = QAction("&Full screen", self,
            shortcut=KeySequenceFullScreen, triggered=self.toggle_full_screen)

        self.zoom_in_action = QAction("Zoom &In", self,
            shortcut=QtGui.QKeySequence.ZoomIn, triggered=self.zoom_in,
            icon=self.style().standardIcon(QtGui.QStyle.SP_ArrowUp))
        self.zoom_out_action = QAction("Zoom &Out", self,
            shortcut=QtGui.QKeySequence.ZoomOut, triggered=self.zoom_out,
            icon=self.style().standardIcon(QtGui.QStyle.SP_ArrowDown))
        self.toogle_zoom_action = QAction("&Toogle Zoom", self,
            shortcut='Z', triggered=self.toggle_zoom)
        self.zoom_home_action = QAction("Fit To Window", self,
            shortcut=QtGui.QKeySequence.MoveToStartOfDocument,
            triggered=self.zoom_home)
        # TODO LH Is F3 (normally meaning 'find next') really the right
        # shortcut for the 'toggle plugin image' action?
        self.toggle_plugin_image_action = QAction(
            "&Display plugin image", self, shortcut="f3",
            triggered=self.toggle_plugin_image,
            statusTip="Display plugin image", checkable=True)

        self.show_specimen_grid_action = QAction('Show grid', self,
            shortcut='g', triggered=self.show_grid)
        self.show_specimen_expanded_action = QAction('Show expanded', self,
            shortcut='e', triggered=self.show_expanded)

        # Help menu
        self.about_action = QAction("&About", self, triggered=self.about)

    def create_menus(self):
        self.toolbar = self.addToolBar("Edit")
        self.toolbar.addAction(self.open_action)
        self.toolbar.addAction(self.save_action)
        for action in [a for a in self.plugin_actions if a.icon()]:
            self.toolbar.addAction(action)
        self.toolbar.addAction(self.zoom_in_action)
        self.toolbar.addAction(self.zoom_out_action)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.view_summary.widget)

        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.open_action)
        self.fileMenu.addAction(self.save_action)
        self.fileMenu.addAction(self.save_crops_action)
        self.fileMenu.addAction(self.export_csv_action)
        self.fileMenu.addAction(self.save_screengrab_action)
        self.fileMenu.addAction(self.close_action)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exit_action)

        self.editMenu = QMenu("&Edit", self)
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
        for action in self.plugin_actions:
            self.editMenu.addAction(action)

        self.viewMenu = QMenu("&View", self)
        self.viewMenu.addAction(self.boxes_view_action)
        self.viewMenu.addAction(self.metadata_view_action)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.full_screen_action)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.zoom_in_action)
        self.viewMenu.addAction(self.zoom_out_action)
        self.viewMenu.addAction(self.toogle_zoom_action)
        self.viewMenu.addAction(self.zoom_home_action)
        self.viewMenu.addAction(self.toggle_plugin_image_action)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.show_specimen_grid_action)
        self.viewMenu.addAction(self.show_specimen_expanded_action)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.about_action)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.editMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)

    def show_tab(self, index):
        self.tabs.setCurrentIndex(index)

    def current_tab_changed(self, index):
        """Slot for self.tabs.currentChanged() signal
        """
        self.sync_ui()

    def selection_changed(self, selected, deselected):
        """Slot for self.grid_view.selectionModel().selectionChanged() signal
        """
        self.sync_ui()

    @report_to_user
    def toggle_full_screen(self):
        """Toggles between full screen and normal
        """
        if self.isFullScreen():
            self.showNormal()

            # When leaving full screen, Qt (or something else) forgets the
            # Mac OS X proxy icon. Clearing and then setting the window file
            # path restores the proxy icon.
            if self.document_path:
                self.setWindowFilePath('')
                self.setWindowFilePath(str(self.document_path))
        else:
            self.showFullScreen()

    def _accept_drag_drop(self, event):
        """If event refers to a single file that can opened, returns the path.
        Returns None otherwise.
        """
        urls = event.mimeData().urls() if event.mimeData() else None
        path = Path(urls[0].toLocalFile()) if urls and 1 == len(urls) else None
        if (path and
            path.suffix in chain([InselectDocument.EXTENSION], IMAGE_SUFFIXES)):
            return urls[0].toLocalFile()
        else:
            return None

    def dragEnterEvent(self, event):
        """QWidget virtual
        """
        debug_print('MainWindow.dragEnterEvent')
        if self._accept_drag_drop(event):
            event.acceptProposedAction()
        else:
            super(MainWindow, self).dragEnterEvent(event)

    def dropEvent(self, event):
        """QWidget virtual
        """
        debug_print('MainWindow.dropEvent')
        res = self._accept_drag_drop(event)
        if res:
            event.acceptProposedAction()
            self.open_file(res)
        else:
            super(MainWindow, self).dropEvent(event)

    def write_geometry_settings(self):
        "Writes geometry to settings"
        debug_print('MainWindow.write_geometry_settings')

        # Taken from http://stackoverflow.com/a/8736705
        # TODO LH Test on multiple display system
        s = QSettings()

        s.setValue("mainwindow/geometry", self.saveGeometry())
        s.setValue("mainwindow/pos", self.pos())
        s.setValue("mainwindow/size", self.size())

    def show_from_geometry_settings(self):
        debug_print('MainWindow.show_from_geometry_settings')

        # TODO LH What if screen resolution, desktop config change or roaming
        # profile means that restored state is outside desktop?
        s = QSettings()

        self.restoreGeometry(s.value("mainwindow/geometry", self.saveGeometry()))
        if not (self.isMaximized() or self.isFullScreen()):
            self.move(s.value("mainwindow/pos", self.pos()))
            self.resize(s.value("mainwindow/size", self.size()))
        self.show()
        # if read_bool("mainwindow/maximized", self.isMaximized()):
        #     debug_print('Will show maximized')
        #     self.showMaximized()
        # elif read_bool("mainwindow/full_screen", self.isMaximized()):
        #     debug_print('Will show full screen')
        #     self.showFullScreen()
        # else:
        #     debug_print('Will show normally')
        #     self.show()

    def sync_ui(self):
        """Synchronise the user interface with the application state
        """
        document = self.document is not None
        has_rows = self.model.rowCount()>0 if self.model else False
        boxes_view_visible = self.boxes_view == self.tabs.currentWidget()
        specimens_view_visible = self.view_specimen == self.tabs.currentWidget()
        has_selection = len(self.view_specimen.selectedIndexes())>0

        # File
        self.save_action.setEnabled(document)
        self.save_crops_action.setEnabled(has_rows)
        self.export_csv_action.setEnabled(has_rows)
        self.close_action.setEnabled(document)

        # Edit
        self.select_all_action.setEnabled(has_rows)
        self.select_none_action.setEnabled(document)
        self.delete_action.setEnabled(has_selection)
        self.next_box_action.setEnabled(has_rows)
        self.previous_box_action.setEnabled(has_rows)
        self.rotate_clockwise_action.setEnabled(has_selection)
        self.rotate_counter_clockwise_action.setEnabled(has_selection)
        for action in self.plugin_actions:
            action.setEnabled(document)

        # View
        self.boxes_view_action.setChecked(boxes_view_visible)
        self.metadata_view_action.setChecked(not boxes_view_visible)
        self.zoom_in_action.setEnabled(document and boxes_view_visible)
        self.zoom_out_action.setEnabled(document and boxes_view_visible)
        self.toogle_zoom_action.setEnabled(document and boxes_view_visible)
        self.zoom_home_action.setEnabled(document and boxes_view_visible)
        self.toggle_plugin_image_action.setEnabled(document and boxes_view_visible)
        self.show_specimen_grid_action.setEnabled(specimens_view_visible)
        self.show_specimen_expanded_action.setEnabled(specimens_view_visible)
