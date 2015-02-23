import cv2
import json
import os
import sys

from functools import partial
from itertools import chain, izip
from pathlib import Path

import numpy as np

from PySide import QtCore, QtGui
from PySide.QtCore import Qt, QEvent
from PySide.QtGui import QMenu, QAction, QMessageBox, QIcon

import inselect.settings

from inselect.lib import utils
from inselect.lib.document import InselectDocument
from inselect.lib.ingest import ingest_image, IMAGE_PATTERNS, IMAGE_SUFFIXES
from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print

import icons        # Register our icon resources with QT

from .help_dialog import HelpDialog
from .model import Model
from .plugins.barcode import BarcodePlugin
from .plugins.segment import SegmentPlugin
from .plugins.subsegment import SubsegmentPlugin
from .roles import RotationRole, RectRole
from .utils import contiguous, report_to_user, qimage_of_bgr
from .views.boxes import BoxesView, GraphicsItemView
from .views.grid import GridView
from .views.metadata import MetadataView
from .views.summary import SummaryView
from .worker_thread import WorkerThread

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
        metadata.setSizes([600, 300])

        if tabbed:
            # Views in tabs
            self.tabs = QtGui.QTabWidget(self)
            self.tabs.addTab(self.boxes_view, 'Boxes')
            self.tabs.addTab(metadata, 'Metadata')
            self.tabs.setCurrentIndex(0)
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
        self.view_grid.installEventFilter(self)
        self.view_metadata.installEventFilter(self)

        self.empty_document()

        self.setAcceptDrops(True)

        if filename:
            self.open_file(filename)

    def eventFilter(self, obj, event):
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
            folder = inselect.settings.get("working_directory")
            filter = u'Inselect documents (*{0});;Images ({1})'
            filter = filter.format(InselectDocument.EXTENSION,
                                   u' '.join(IMAGE_PATTERNS))
            path, selectedFilter = QtGui.QFileDialog.getOpenFileName(
                self, "Open", folder, filter)

        if path:
            # Will be None if user cancelled getOpenFileName
            if not self.close_document():
                # User does not want to close the existing document
                pass
            else:
                path = Path(path)
                inselect.settings.set_value('working_directory', str(path.parent))
                if path.suffix in IMAGE_SUFFIXES:
                    # Compute the path to the inselect document (which may or
                    # may not already exist) of the image file
                    doc_of_image = path.name.replace(InselectDocument.THUMBNAIL_SUFFIX, u'')
                    doc_of_image = path.parent / doc_of_image
                    doc_of_image = doc_of_image.with_suffix(InselectDocument.EXTENSION)
                else:
                    doc_of_image = None

                if InselectDocument.EXTENSION == path.suffix:
                    # Open the .inselect document
                    debug_print('Opening inselect document [{0}]'.format(path))
                    self.open_document(path)
                elif doc_of_image and doc_of_image.is_file():
                    # An image file corresponding to an existing .inselect file
                    msg = u'Opening inselect document [{0}] of thumbnail [{1}]'
                    debug_print(msg.format(doc_of_image, path))
                    self.open_document(doc_of_image)
                elif path.suffix in IMAGE_SUFFIXES:
                    msg = u'Creating new inselect document for image [{0}]'
                    debug_print(msg.format(path))
                    self.new_document(path)
                else:
                    raise InselectError('Unknown file type [{0}]'.format(path))

    def new_document(self, path):
        """Creates and opens a new inselect document for the scanned image
        given in path
        """
        debug_print('MainWindow.new_document [{0}]'.format(path))

        # Callable for worker thread
        class NewDoc(object):
            def __init__(self, image):
                self.image = image

            def __call__(self, progress):
                progress('Creating thumbnail of scanned image')
                doc = ingest_image(self.image, self.image.parent)
                self.document_path = doc.document_path

        self.run_in_worker(NewDoc(Path(path)), 'New document',
                           self.new_document_finished)

    def new_document_finished(self, operation):
        """Called when new_document worker has finished
        """
        debug_print('MainWindow.new_document_finished')

        document_path = operation.document_path
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
        inselect.settings.set_value('working_directory', str(path.parent))

        self.document = document
        self.document_path = path
        self.model.from_document(self.document)

        # TODO LH Prefer setWindowFilePath to setWindowTitle?
        self.setWindowTitle(u"Inselect [{0}]".format(self.document_path.stem))

        self.sync_ui()

    @report_to_user
    def save_document(self):
        """Saves the document
        """
        debug_print('MainWindow.save_document')
        items = []

        self.model.to_document(self.document)
        self.document.save()
        self.model.clear_modified()

    @report_to_user
    def save_crops(self):
        """Saves cropped specimen images
        """
        debug_print('MainWindow.save_crops')
        res = QMessageBox.Yes
        existing_crops = self.document.crops_dir.is_dir()

        if existing_crops:
            # TODO LH Prompt should mention that full-res scan will need to be
            # loaded
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
            self.document.export_csv(path)
            msg = "Data for {0} boxes written to {1}"
            msg = msg.format(self.document.n_items, path)
            QMessageBox.information(self, "CSV saved", msg)

    @report_to_user
    def close_document(self):
        """Closes the document and returns True if not modified or if modified
        and user does not cancel. Does not close the document and returns False
        if modified and users cancels.
        """
        debug_print('MainWindow.close_document')
        if self.model.modified:
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
        self.plugin_image = None
        self.plugin_image_visible = False
        self.model.clear()

        # TODO LH Prefer setWindowFilePath to setWindowTitle?
        self.setWindowTitle("Inselect")

        self.sync_ui()

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
    def about(self):
        QMessageBox.about(
            self,
            inselect.settings.get('about_label'),
            inselect.settings.get('about_text')
        )

    @report_to_user
    def help(self):
        """Open the help dialog"""
        d = HelpDialog(self)
        d.exec_()

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
                                    '{0} cancelled'.format(name))
        elif error_message:
            QMessageBox.information(self,
                    'An error occurred running'.format(name),
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
        sm = self.view_grid.selectionModel()
        m = self.model
        sm.select(QtGui.QItemSelection(m.index(0, 0), m.index(m.rowCount()-1, 0)),
                  QtGui.QItemSelectionModel.Select)

    @report_to_user
    def select_none(self):
        sm = self.view_grid.selectionModel()
        sm.select(QtGui.QItemSelection(), QtGui.QItemSelectionModel.Clear)

    @report_to_user
    def delete_selected(self):
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
            shortcut="N", triggered=partial(self.select_next, forwards=True))
        self.previous_box_action = QAction("Previous box", self,
            shortcut="P", triggered=partial(self.select_next, forwards=False))
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
        self.metadata_view_action = QAction("&Metadata", self, checkable=True,
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
        # shortcut for the toggle segment image action?
        self.toggle_plugin_image_action = QAction(
            "&Display plugin image", self, shortcut="f3",
            triggered=self.toggle_plugin_image,
            statusTip="Display plugin image", checkable=True)

        # Help menu
        self.about_action = QAction("&About", self, triggered=self.about)
        self.help_action = QAction("&Help", self,
            shortcut=QtGui.QKeySequence.HelpContents, triggered=self.help)

    def create_menus(self):
        self.toolbar = self.addToolBar("Edit")
        self.toolbar.addAction(self.open_action)
        self.toolbar.addAction(self.save_action)
        for action in [a for a in self.plugin_actions if a.icon()]:
            self.toolbar.addAction(action)
        self.toolbar.addAction(self.zoom_in_action)
        self.toolbar.addAction(self.zoom_out_action)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.open_action)
        self.fileMenu.addAction(self.save_action)
        self.fileMenu.addAction(self.save_crops_action)
        self.fileMenu.addAction(self.export_csv_action)
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
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.toggle_plugin_image_action)

        self.helpMenu = QMenu("&Help", self)
        self.helpMenu.addAction(self.help_action)
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

    def sync_ui(self):
        """Synchronise the user interface with the application state
        """
        document = self.document is not None
        has_rows = self.model.rowCount()>0 if self.model else False
        boxes_view_visible = self.boxes_view == self.tabs.currentWidget()
        has_selection = len(self.view_grid.selectedIndexes())>0

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
