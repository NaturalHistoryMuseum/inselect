import sys

from functools import partial
from itertools import count, izip
from pathlib import Path

from PySide import QtGui
from PySide.QtCore import Qt, QEvent, QSettings
from PySide.QtGui import (QMenu, QAction, QMessageBox, QDesktopServices,
                          QVBoxLayout, QWidget)

# This import is to register our icon resources with QT
import inselect.gui.icons  # noqa

from inselect.lib.document import InselectDocument
from inselect.lib.document_export import DocumentExport
from inselect.lib.ingest import ingest_image, IMAGE_PATTERNS, IMAGE_SUFFIXES_RE
from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print, is_writable

from .about import show_about_box
from .colours import colour_scheme_choice
from .info_widget import InfoWidget
from .cookie_cutter_choice import cookie_cutter_choice
from .cookie_cutter_widget import CookieCutterWidget
from .format_validation_problems import format_validation_problems
from .model import Model
from .plugins.barcode import BarcodePlugin
from .plugins.segment import SegmentPlugin
from .plugins.subsegment import SubsegmentPlugin
from .recent_documents import RecentDocuments
from .roles import RotationRole
from .user_template_choice import user_template_choice
from .utils import contiguous, report_to_user, qimage_of_bgr
from .views.boxes import BoxesView, GraphicsItemView
from .views.metadata import MetadataView
from .views.object import ObjectView
from .views.selector import SelectorView
from .views.summary import SummaryView
from .worker_thread import WorkerThread


class MainWindow(QtGui.QMainWindow):
    """The application's main window
    """
    DOCUMENT_FILE_FILTER = u'Inselect documents (*{0});;Images ({1})'.format(
        InselectDocument.EXTENSION,
        u' '.join(IMAGE_PATTERNS)
    )

    IMAGE_FILE_FILTER = u'Images ({0})'.format(u' '.join(IMAGE_PATTERNS))

    def __init__(self, app, filename=None):
        super(MainWindow, self).__init__()
        self.app = app

        # Boxes view
        self.view_graphics_item = GraphicsItemView()
        # self.boxes_view is a QGraphicsView, not a QAbstractItemView
        self.boxes_view = BoxesView(self.view_graphics_item.scene)

        # Object, metadata and summary views
        self.view_metadata = MetadataView()
        self.view_object = ObjectView()
        self.view_summary = SummaryView()
        self.view_selector = SelectorView()

        # Views in tabs
        self.tabs = QtGui.QTabWidget()
        self.tabs.addTab(self.boxes_view, 'Boxes')
        self.tabs.addTab(self.view_object, 'Objects')
        self.tabs.setCurrentIndex(0)

        # Information about the loaded document
        self.info_widget = InfoWidget()

        # Cookie cutter widget
        self.cookie_cutter_widget = CookieCutterWidget()
        self.cookie_cutter_widget.save_to_new_action.triggered.connect(
            self.save_to_cookie_cutter
        )
        self.cookie_cutter_widget.apply_current_action.triggered.connect(
            self.apply_cookie_cutter
        )
        cookie_cutter_choice().cookie_cutter_changed.connect(
            self.new_cookie_cutter
        )

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
        self.view_object.setModel(self.model)
        self.view_summary.setModel(self.model)
        self.view_selector.setModel(self.model)

        # A consistent selection across all views
        sm = self.view_object.selectionModel()
        self.view_graphics_item.setSelectionModel(sm)
        self.view_metadata.setSelectionModel(sm)
        self.view_summary.setSelectionModel(sm)
        self.view_selector.setSelectionModel(sm)

        # Plugins
        self.plugins = (SegmentPlugin, SubsegmentPlugin, BarcodePlugin)
        # QActions. Populated in self.create_menu_actions()
        self.plugin_actions = len(self.plugins) * [None]
        # QActions. Populated in self.create_menu_actions()
        self.plugin_config_ui_actions = len(self.plugins) * [None]
        self.plugin_image = None
        self.plugin_image_visible = False

        # Colour scheme QActions. Populated in self.create_actions()
        self.colour_scheme_actions = []

        # Long-running operations are run in their own thread.
        self.running_operation = None

        self.create_menu_actions()
        self.create_non_menu_actions()
        self.create_toolbar()
        self.create_menus()

        # Conect signals
        self.tabs.currentChanged.connect(self.current_tab_changed)
        sm.selectionChanged.connect(self.selection_changed)
        colour_scheme_choice().colour_scheme_changed.connect(
            self.colour_scheme_changed
        )

        # Filter events
        self.tabs.installEventFilter(self)
        self.boxes_view.installEventFilter(self)
        self.view_metadata.installEventFilter(self)
        self.view_object.installEventFilter(self)
        self.view_summary.installEventFilter(self)
        self.view_selector.installEventFilter(self)

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
            folder = QSettings().value(
                'working_directory',
                QDesktopServices.storageLocation(QDesktopServices.DocumentsLocation)
            )

            path, selectedFilter = QtGui.QFileDialog.getOpenFileName(
                self, "Open", folder, self.DOCUMENT_FILE_FILTER)

        # path will be None if user cancelled getOpenFileName
        if path:
            path = Path(path)

            # What type of file did the user select?
            document_path = image_path = None
            if InselectDocument.EXTENSION == path.suffix:
                # An inselect document
                document_path = path
            elif IMAGE_SUFFIXES_RE.match(path.name):
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
                self.open_document(path=document_path)
            elif image_path:
                msg = u'Creating new inselect document for image [{0}]'
                debug_print(msg.format(image_path))
                self.new_document(image_path)
            else:
                raise InselectError('Unknown file type [{0}]'.format(path))

    def new_document(self, path, default_metadata_items=None):
        """Creates and opens a new inselect document for the scanned image
        given in path
        """
        debug_print('MainWindow.new_document [{0}]'.format(path))

        path = Path(path)
        if not path.is_file():
            raise InselectError(u'Image file [{0}] does not exist'.format(path))
        else:
            # Callable for worker thread
            thumbnail_width = user_template_choice().current.thumbnail_width_pixels

            class NewDoc(object):
                def __init__(self, image, default_metadata_items):
                    self.image = image
                    self.default_metadata_items = default_metadata_items
                    self.document = None

                def __call__(self, progress):
                    progress('Creating thumbnail of scanned image')
                    doc = ingest_image(self.image, self.image.parent,
                                       thumbnail_width,
                                       self.default_metadata_items,
                                       cookie_cutter_choice().current)
                    self.document = doc

            self.run_in_worker(NewDoc(path, default_metadata_items),
                               'New document',
                               self.new_document_finished)

    def new_document_finished(self, operation):
        """Called when new_document worker has finished
        """
        debug_print('MainWindow.new_document_finished')

        document = operation.document
        document_path = document.document_path
        QSettings().setValue('working_directory', str(document_path.parent))

        self.open_document(document=document)

        msg = u'New Inselect document [{0}] created in [{1}]'
        msg = msg.format(document_path.stem, document_path.parent)
        QMessageBox.information(self, "Document created", msg)

    def _sync_recent_documents_actions(self):
        "Synchronises the 'recent documents' actions"
        debug_print('MainWindow._sync_recent_documents_actions')
        recent = RecentDocuments().read_paths()
        if not recent:
            # No recent documents - a single disabled action with placeholder
            # text
            self.recent_doc_actions[0].setEnabled(False)
            self.recent_doc_actions[0].setText('No recent documents')
            self.recent_doc_actions[0].setVisible(True)
            hide_actions_after = 1
        elif len(recent) > len(self.recent_doc_actions):
            msg = 'Unexpected number of recent documents [{0}]'
            raise ValueError(msg.format(len(recent)))
        else:
            # Show as many actions as there are recent documents
            for index, path, action in izip(count(), recent, self.recent_doc_actions):
                action.setEnabled(True)
                action.setText(path.stem)
                action.setToolTip(str(path))
                action.setVisible(True)
            hide_actions_after = 1 + index

        # Hide all actions after and including 'hide_actions_after'
        for action in self.recent_doc_actions[hide_actions_after:]:
            action.setVisible(False)
            action.setText('')

    @report_to_user
    def open_recent(self, index):
        debug_print('MainWindow._open_recent [{0}]'.format(index))
        recent = RecentDocuments().read_paths()
        self.open_file(recent[index])

    def open_document(self, path=None, document=None):
        """Either loads the inselect document from  path or uses the existing
        InselectDocument given in document.
        """
        if path and document:
            raise ValueError('Both path and document given')

        if path:
            path = Path(path)
            document = InselectDocument.load(path)
        else:
            path = document.document_path

        debug_print('MainWindow.open_document [{0}]'.format(path))
        QSettings().setValue("working_directory", str(path.parent))

        self.document = document
        self.document_path = path
        self.model.from_document(self.document)

        self.setWindowTitle('')
        self.setWindowFilePath(str(self.document_path))
        self.info_widget.set_document(self.document)

        RecentDocuments().add_path(path)
        self._sync_recent_documents_actions()

        self.sync_ui()

        if not is_writable(path):
            msg = (u'The file [{0}] is read-only.\n\n'
                   u'You will not be able to save any changes that you make.')
            msg = msg.format(path.name)
            QMessageBox.warning(self, "Document is read-only", msg)

    @report_to_user
    def save_document(self):
        """Saves the document
        """
        debug_print('MainWindow.save_document')

        self.model.to_document(self.document)
        self.document.save()
        self.model.set_modified(False)
        self.info_widget.set_document(self.document)

    def _prompt_validation_problems(self, problems, title, question):
        """Prompts the user with the question and the list of validation
        problems. Returns the result of QMessageBox.exec_().
        """
        box = QMessageBox(QMessageBox.Question, title, '',
                          QMessageBox.No | QMessageBox.Yes)
        box.setDefaultButton(QtGui.QMessageBox.No)

        SHOW_AT_MOST = 5
        report_problems = problems[:SHOW_AT_MOST]
        if SHOW_AT_MOST <= len(problems):
            msg = ('The document contains {n_problems} validation problems. '
                   'The first {show_at_most} are shown below. Click "Show '
                   'details" to see all of them.\n'
                   '\n'
                   '{problems}\n'
                   '\n'
                   '{question}')
            box.setDetailedText('\n'.join(problems))
        else:
            msg = ('The document contains {n_problems} validation problems:\n'
                   '\n'
                   '{problems}\n'
                   '\n'
                   '{question}')

        box.setText(msg.format(n_problems=len(problems),
                               show_at_most=SHOW_AT_MOST,
                               problems='\n'.join(report_problems),
                               question=question))

        return box.exec_()

    @report_to_user
    def save_crops(self, user_template=None):
        """Saves cropped object images
        """
        debug_print('MainWindow.save_crops')

        if user_template:
            export = DocumentExport(user_template)
        else:
            export = DocumentExport(user_template_choice().current)

        self.model.to_document(self.document)

        crops_dir = export.crops_dir(self.document)

        res = QMessageBox.Yes
        if crops_dir.is_dir():
            msg = 'Overwrite the existing object images?'
            res = QMessageBox.question(self, 'Save object images?',
                                       msg, QMessageBox.No, QMessageBox.Yes)

        validation = export.validation_problems(self.document)
        if QMessageBox.Yes == res and validation and validation.any_problems:
            res = self._prompt_validation_problems(
                list(format_validation_problems(validation)),
                'Save object images?',
                'Would you like to save the object images?')

        if QMessageBox.Yes == res:
            def save_crops(progress):
                progress('Loading full-resolution scanned image')
                self.document.scanned.array

                progress('Saving crops')
                export.save_crops(self.document, progress)

            def completed(operation):
                QMessageBox.information(self, "Crops saved", msg)

            msg = "{0} crops saved in {1}"
            msg = msg.format(self.document.n_items, crops_dir)
            self.run_in_worker(save_crops, 'Save crops', completed)

    @report_to_user
    def export_csv(self, user_template=None):
        debug_print('MainWindow.export_csv')

        if user_template:
            export = DocumentExport(user_template)
        else:
            export = DocumentExport(user_template_choice().current)

        self.model.to_document(self.document)
        path = export.csv_path(self.document)

        res = QMessageBox.Yes
        existing_csv = path.is_file()

        if existing_csv:
            msg = 'Overwrite the existing CSV file?'
            res = QMessageBox.question(self, 'Export CSV file?',
                                       msg, QMessageBox.No, QMessageBox.Yes)

        validation = export.validation_problems(self.document)
        if QMessageBox.Yes == res and validation and validation.any_problems:
            res = self._prompt_validation_problems(
                list(format_validation_problems(validation)),
                'Export CSV file?',
                'Would you like to export a CSV file?')

        if QMessageBox.Yes == res:
            export.export_csv(self.document)
            msg = "Data for {0} boxes written to {1}"
            msg = msg.format(self.document.n_items, path)
            QMessageBox.information(self, "CSV saved", msg)

    @report_to_user
    def save_screengrab(self):
        """Prompts the user for the image file path to which to a screenshot
        will be saved.
        """
        debug_print('MainWindow.save_screengrab')

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

        if self.document_path:
            # Default name is the name of this document with '_screengrab' appended
            default_fname = u'{0}_screengrab'.format(self.document_path.stem)
        else:
            default_fname = u'inselect_screengrab'

        # Default suffix is jpg, if available
        for e in ('.jpg', '.jpeg', '.png'):
            if '*{0}'.format(e) in extensions:
                default_extension = e
                break
        else:
            # Use the first available extension
            default_extension = extensions[0][1:]

        default_fname = Path(default_fname).with_suffix(default_extension)

        # Default folder is the user's documents folder
        default_dir = QDesktopServices.storageLocation(
            QDesktopServices.DocumentsLocation
        )

        debug_print(u'Default screengrab dir [{0}]'.format(default_dir))
        debug_print(u'Default screengrab fname [{0}]'.format(default_fname))
        path, selected_filter = QtGui.QFileDialog.getSaveFileName(
            self, "Save image file of boxes view",
            unicode(Path(default_dir) / default_fname),
            filter=filter
        )

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
            res = QMessageBox.question(
                self, 'Save document?',
                'Save the document before closing?',
                (QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel),
                QMessageBox.Yes
            )

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
        # Clear selection before closing for performance reasons
        self.select_none()
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
        self.view_object.show_grid()

    @report_to_user
    def show_expanded(self):
        self.view_object.show_expanded()

    @report_to_user
    def about(self):
        show_about_box(self)

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

            # TODO Make this a namedtuple
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
            QMessageBox.information(
                self,
                "An error occurred running '{0}'".format(name),
                error_message + '\n\nExisting data has not been altered'
            )
        else:
            if complete_fn:
                complete_fn(operation)
            self.sync_ui()

    @report_to_user
    def run_plugin(self, plugin_number):
        """Passes each cropped object image through plugin
        """
        debug_print("MainWindow.run_plugin")

        if plugin_number < 0 or plugin_number > len(self.plugins):
            raise ValueError('Unexpected plugin [{0}]'.format(plugin_number))
        else:
            plugin = self.plugins[plugin_number]

            self.model.to_document(self.document)

            # Create the plugin
            operation = plugin(self.document, self)
            if operation.can_be_run():
                self.run_in_worker(operation,
                                   plugin.NAME,
                                   self.plugin_finished)
            else:
                pass

    @report_to_user
    def show_plugin_config(self, plugin_number):
        debug_print("MainWindow.show_plugin_config")

        if (plugin_number < 0 or plugin_number > len(self.plugins) or
                self.plugin_config_ui_actions[plugin_number] is None):
            raise ValueError('Unexpected plugin [{0}]'.format(plugin_number))
        else:
            self.plugins[plugin_number].config(self)

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
        sm = self.view_object.selectionModel()
        m = self.model
        sm.select(QtGui.QItemSelection(m.index(0, 0), m.index(m.rowCount()-1, 0)),
                  QtGui.QItemSelectionModel.Select)

    @report_to_user
    def select_none(self):
        sm = self.view_object.selectionModel()
        sm.select(QtGui.QItemSelection(), QtGui.QItemSelectionModel.Clear)

    @report_to_user
    def delete_selected(self):
        """Deletes the selected boxes
        """
        debug_print('MainWindow.delete_selected')

        # Delete contiguous blocks of rows
        selected = self.view_object.selectionModel().selectedIndexes()
        selected = sorted([i.row() for i in selected])

        # Remove blocks in reverse order so that row indices are not invalidated
        # TODO LH We shouldn't need to remove blocks in reverse order - stems
        # from crummy GraphicsItemView
        for first, n_rows in reversed(list(contiguous(selected))):
            self.model.removeRows(first, n_rows)

        # Prevent object view from scrolling to the top of the view. The natural
        # place to do this is within ObjectView but I was unable to get that
        # solution to work.
        self.view_object.scrollTo(self.view_object.currentIndex())

    @report_to_user
    def select_next_prev(self, next):
        """Selects the next box in the mode if next is True, the previous
        box in the model if next if False.
        """
        sm = self.view_object.selectionModel()
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
    def select_by_size_step(self, larger=False):
        """Step the 'select by size' slider
        """
        self.view_selector.single_step(larger)

    @report_to_user
    def rotate90(self, clockwise):
        """Rotates the selected boxes 90 either clockwise or counter-clockwise.
        """
        debug_print('MainWindow.rotate')
        value = 90 if clockwise else -90
        selected = self.view_object.selectionModel().selectedIndexes()
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

    def create_menu_actions(self):
        """Creates actions that are associated with menu items
        """
        # File menu
        self.open_action = QAction(
            "&Open...", self,
            shortcut=QtGui.QKeySequence.Open, triggered=self.open_file,
            icon=self.style().standardIcon(QtGui.QStyle.SP_DialogOpenButton)
        )
        self.copy_to_new_document_action = QAction(
            "Copy to new document...", self,
            triggered=self.copy_to_new_document
        )
        self.save_action = QAction(
            "&Save", self,
            shortcut=QtGui.QKeySequence.Save, triggered=self.save_document,
            icon=self.style().standardIcon(QtGui.QStyle.SP_DialogSaveButton)
        )
        self.save_crops_action = QAction(
            "&Save crops", self,
            triggered=self.save_crops
        )
        self.export_csv_action = QAction(
            "&Export CSV", self,
            triggered=self.export_csv
        )
        self.save_screengrab_action = QAction(
            "Save screen grab", self,
            triggered=self.save_screengrab
        )
        self.close_action = QAction(
            "&Close", self,
            shortcut=QtGui.QKeySequence.Close, triggered=self.close_document
        )
        self.exit_action = QAction(
            "E&xit", self,
            shortcut=QtGui.QKeySequence.Quit, triggered=self.close
        )

        if 'win32' == sys.platform:
            # Support ctrl+w and ctrl+q on Windows
            self.close_action.setShortcuts(['ctrl+w',
                                            self.close_action.shortcut()])
            self.exit_action.setShortcuts(['ctrl+q',
                                           self.exit_action.shortcut()])

        self.recent_doc_actions = [None] * RecentDocuments.MAX_RECENT_DOCS
        for index in xrange(RecentDocuments.MAX_RECENT_DOCS):
            self.recent_doc_actions[index] = QAction(
                'Recent document', self,
                triggered=partial(self.open_recent, index)
            )
        self._sync_recent_documents_actions()

        # Edit menu
        self.select_all_action = QAction(
            "Select &All", self,
            shortcut=QtGui.QKeySequence.SelectAll, triggered=self.select_all
        )
        # QT does not provide a 'select none' key sequence
        self.select_none_action = QAction(
            "Select &None", self,
            shortcut="ctrl+D", triggered=self.select_none
        )
        self.next_box_action = QAction(
            "Next box", self, shortcut="ctrl+N",
            triggered=partial(self.select_next_prev, next=True)
        )
        self.previous_box_action = QAction(
            "Previous box", self,
            shortcut="ctrl+P",
            triggered=partial(self.select_next_prev, next=False)
        )
        self.select_by_size_larger_action = QAction(
            "Select increasing size", self, shortcut="ctrl+>",
            triggered=partial(self.select_by_size_step, larger=True)
        )
        self.select_by_size_smaller_action = QAction(
            "Select decreasing size", self, shortcut="ctrl+<",
            triggered=partial(self.select_by_size_step, larger=False)
        )

        self.delete_action = QAction(
            "&Delete selected", self,
            shortcut=QtGui.QKeySequence.Delete,
            triggered=self.delete_selected
        )
        # CMD + backspace is the Mac OS X shortcut for delete. Some Mac
        # keyboards have a Delete key, so this standard shortcut is also
        # included.
        if 'darwin' == sys.platform:
            self.delete_action.setShortcuts(['ctrl+backspace',
                                             self.delete_action.shortcut()])

        self.rotate_clockwise_action = QAction(
            "Rotate clockwise", self, shortcut="ctrl+R",
            triggered=partial(self.rotate90, clockwise=True)
        )
        self.rotate_counter_clockwise_action = QAction(
            "Rotate counter-clockwise", self, shortcut="ctrl+L",
            triggered=partial(self.rotate90, clockwise=False)
        )

        # Plugins
        # Plugin shortcuts start at F5
        shortcut_offset = 5
        for index, plugin in enumerate(self.plugins):
            action = QAction(plugin.NAME, self,
                             triggered=partial(self.run_plugin, index))
            shortcut_fkey = index + shortcut_offset
            if shortcut_fkey < 13:
                # Keyboards typically have 12 function keys
                action.setShortcut('f{0}'.format(shortcut_fkey))
            if hasattr(plugin, 'icon'):
                action.setIcon(plugin.icon())
            self.plugin_actions[index] = action
            if hasattr(plugin, 'config'):
                ui_action = QAction(
                    u"Configure '{0}'...".format(plugin.NAME), self,
                    triggered=partial(self.show_plugin_config, index)
                )
                # Force menu items to appear on Mac
                ui_action.setMenuRole(QAction.NoRole)
                self.plugin_config_ui_actions[index] = ui_action

        # View menu
        # It is tempting to set the trigger to
        # partial(self.tabs.setCurrentIndex, 0) but this causes a segfault when
        # the application exits on linux. It also means that exceptions will be
        # silently swallowed.
        self.boxes_view_action = QAction(
            "&Boxes", self, checkable=True, triggered=partial(self.show_tab, 0),
            shortcut='ctrl+B'
        )
        self.metadata_view_action = QAction(
            "Ob&jects", self, checkable=True,
            triggered=partial(self.show_tab, 1), shortcut='ctrl+j'
        )

        # FullScreen added in Qt 5.something
        # https://qt.gitorious.org/qt/qtbase-miniak/commit/1ef8a6d
        if not hasattr(QtGui.QKeySequence, 'FullScreen'):
            if 'darwin' == sys.platform:
                KeySequenceFullScreen = 'shift+ctrl+f'
            else:
                KeySequenceFullScreen = 'f11'
        else:
            KeySequenceFullScreen = QtGui.QKeySequence.FullScreen
        self.full_screen_action = QAction(
            "&Full screen", self, shortcut=KeySequenceFullScreen,
            triggered=self.toggle_full_screen
        )

        self.zoom_in_action = QAction(
            "Zoom &In", self, shortcut=QtGui.QKeySequence.ZoomIn,
            triggered=self.zoom_in,
            icon=self.style().standardIcon(QtGui.QStyle.SP_ArrowUp)
        )
        self.zoom_out_action = QAction(
            "Zoom &Out", self, shortcut=QtGui.QKeySequence.ZoomOut,
            triggered=self.zoom_out,
            icon=self.style().standardIcon(QtGui.QStyle.SP_ArrowDown)
        )
        self.toogle_zoom_action = QAction(
            "&Toogle Zoom", self, shortcut='Z', triggered=self.toggle_zoom
        )
        self.zoom_home_action = QAction(
            "Fit To Window", self,
            shortcut=QtGui.QKeySequence.MoveToStartOfDocument,
            triggered=self.zoom_home
        )
        # TODO LH Is F3 (normally meaning 'find next') really the right
        # shortcut for the 'toggle plugin image' action?
        self.toggle_plugin_image_action = QAction(
            "&Display plugin image", self, shortcut="f3",
            triggered=self.toggle_plugin_image,
            statusTip="Display plugin image", checkable=True
        )

        self.show_object_grid_action = QAction(
            'Show grid', self, shortcut='ctrl+G', triggered=self.show_grid
        )
        self.show_object_expanded_action = QAction(
            'Show expanded', self,
            shortcut='ctrl+E', triggered=self.show_expanded
        )

        # Colours
        for name in colour_scheme_choice().colour_scheme_names():
            action = QAction(name, self, checkable=True,
                             triggered=partial(self.set_colour_scheme, name))
            self.colour_scheme_actions.append(action)

        # Help menu
        self.about_action = QAction("&About", self, triggered=self.about)

    def create_non_menu_actions(self):
        """Creates actions that are not associated with menu items
        """
        # Menu-less actions
        # Shortcuts for next / previous tab
        self.previous_tab_action = QAction(
            "Previous tab", self, triggered=partial(self.next_previous_tab, False),
            shortcut='ctrl+PgDown'
        )
        self.next_tab_action = QAction(
            "Next tab", self, triggered=partial(self.next_previous_tab, True),
            shortcut='ctrl+PgUp'
        )

        # Mac also uses these funny shortcuts
        if 'darwin' == sys.platform:
            self.previous_tab_action.setShortcuts(
                ['shift+ctrl+[', self.previous_tab_action.shortcut()]
            )
            self.next_tab_action.setShortcuts(
                ['shift+ctrl+]', self.next_tab_action.shortcut()]
            )

        self.addAction(self.previous_tab_action)
        self.addAction(self.next_tab_action)

    def create_toolbar(self):
        """Creates the toolbar
        """
        self.toolbar = self.addToolBar("Edit")
        self.toolbar.addAction(self.open_action)
        self.toolbar.addAction(self.save_action)
        for action in filter(lambda a: a.icon(), self.plugin_actions):
            self.toolbar.addAction(action)
        self.toolbar.addAction(self.zoom_in_action)
        self.toolbar.addAction(self.zoom_out_action)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolbar.addWidget(self.cookie_cutter_widget)

        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.view_summary.widget)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.view_selector.widget)

    def create_menus(self):
        """Create menu items
        """
        self._file_menu = QMenu("&File", self)
        self._file_menu.addAction(self.open_action)
        recent = self._file_menu.addMenu('Recent documents')
        for action in self.recent_doc_actions:
            recent.addAction(action)
        self._file_menu.addAction(self.copy_to_new_document_action)
        self._file_menu.addAction(self.save_action)
        self._file_menu.addAction(self.close_action)
        self._file_menu.addSeparator()
        self._file_menu.addAction(self.save_crops_action)
        self._file_menu.addAction(self.export_csv_action)
        self._file_menu.addSeparator()
        self._file_menu.addAction(self.save_screengrab_action)
        self._file_menu.addSeparator()
        self._file_menu.addAction(self.exit_action)

        self._edit_menu = QMenu("&Edit", self)
        self._edit_menu.addAction(self.select_all_action)
        self._edit_menu.addAction(self.select_none_action)
        self._edit_menu.addAction(self.delete_action)
        self._edit_menu.addSeparator()
        self._edit_menu.addAction(self.next_box_action)
        self._edit_menu.addAction(self.previous_box_action)
        self._edit_menu.addAction(self.select_by_size_larger_action)
        self._edit_menu.addAction(self.select_by_size_smaller_action)
        self._edit_menu.addSeparator()
        self._edit_menu.addAction(self.rotate_clockwise_action)
        self._edit_menu.addAction(self.rotate_counter_clockwise_action)
        self._edit_menu.addSeparator()
        user_template_popup = self._edit_menu.addMenu('Metadata template')
        self.view_metadata.popup_button.inject_actions(user_template_popup)
        self._edit_menu.addSeparator()
        cookie_cutter_popup = self._edit_menu.addMenu('Cookie cutter')
        self.cookie_cutter_widget.inject_actions(cookie_cutter_popup)
        self._edit_menu.addSeparator()
        for action in self.plugin_actions:
            self._edit_menu.addAction(action)
        for action in (a for a in self.plugin_config_ui_actions if a):
            self._edit_menu.addAction(action)

        self._view_menu = QMenu("&View", self)
        self._view_menu.addAction(self.boxes_view_action)
        self._view_menu.addAction(self.metadata_view_action)
        self._view_menu.addSeparator()
        self._view_menu.addAction(self.full_screen_action)
        self._view_menu.addSeparator()
        self._view_menu.addAction(self.zoom_in_action)
        self._view_menu.addAction(self.zoom_out_action)
        self._view_menu.addAction(self.toogle_zoom_action)
        self._view_menu.addAction(self.zoom_home_action)
        self._view_menu.addAction(self.toggle_plugin_image_action)
        self._view_menu.addSeparator()
        self._view_menu.addAction(self.show_object_grid_action)
        self._view_menu.addAction(self.show_object_expanded_action)
        self._view_menu.addSeparator()
        colours_popup = self._view_menu.addMenu('Colour scheme')
        for action in self.colour_scheme_actions:
            colours_popup.addAction(action)

        self._help_menu = QMenu("&Help", self)
        self._help_menu.addAction(self.about_action)

        self.menuBar().addMenu(self._file_menu)
        self.menuBar().addMenu(self._edit_menu)
        self.menuBar().addMenu(self._view_menu)
        self.menuBar().addMenu(self._help_menu)

    @report_to_user
    def show_tab(self, index):
        self.tabs.setCurrentIndex(index)

    @report_to_user
    def next_previous_tab(self, next):
        """Selects the next (if next if True) or previous (if next if False) tab
        """
        select = self.tabs.currentIndex()
        select += 1 if next else -1
        if select == self.tabs.count():
            select = 0
        elif select < 0:
            select = self.tabs.count() - 1
        self.tabs.setCurrentIndex(select)

    def current_tab_changed(self, index):
        """Slot for self.tabs.currentChanged() signal
        """
        self.sync_ui()

    def selection_changed(self, selected, deselected):
        """Slot for self.grid_view.selectionModel().selectionChanged() signal
        """
        self.sync_ui()

    def colour_scheme_changed(self):
        """Slot for COLOUR_SCHEME_CHANGED signal
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

    @report_to_user
    def set_colour_scheme(self, name):
        "Sets the colour scheme"
        colour_scheme_choice().set_colour_scheme(name)

    def new_cookie_cutter(self):
        """Slot for cookie_cutter_changed signal - sets menu and button text
        """
        debug_print('MainWindow.new_cookie_cutter')
        self.sync_ui()

    @report_to_user
    def save_to_cookie_cutter(self):
        "Saves bounding boxes to a new 'cookie cutter' file"
        folder = unicode(cookie_cutter_choice().last_directory())
        path, selectedFilter = QtGui.QFileDialog.getSaveFileName(
            self, "New cookie cutter", folder,
            CookieCutterWidget.FILE_FILTER
        )

        if path:
            # Save the user's choice
            self.model.to_document(self.document)
            cookie_cutter_choice().create_and_use(
                [tuple(v['rect']) for v in self.document.items],
                path
            )

    @report_to_user
    def apply_cookie_cutter(self):
        """Replaces existing boxes with those in cookie_cutter_choice.
        """
        debug_print('MainWindow.apply_cookie_cutter')
        if self.model.rowCount():
            msg = ('Applying the cookie cutter will cause all boxes and '
                   'metadata to be replaced.\n\nContinue and replace all '
                   'existing boxes and metadata?')
            res = QMessageBox.question(self, 'Replace boxes?', msg,
                                       QMessageBox.No, QMessageBox.Yes)
        else:
            res = QMessageBox.Yes

        if QMessageBox.Yes == res:
            self.model.set_new_boxes(
                cookie_cutter_choice().current.document_items
            )

    @report_to_user
    def copy_to_new_document(self):
        """Prompts the user to choose an image, creates an inselect document
        for the selected image, copies metadata from the currently open
        document to the new document and finally opens the new document
        """
        debug_print('MainWindow.copy_to_new_document')

        folder = QSettings().value(
            'working_directory',
            QDesktopServices.storageLocation(QDesktopServices.DocumentsLocation)
        )

        path, selectedFilter = QtGui.QFileDialog.getOpenFileName(
            self, "Open", folder, self.IMAGE_FILE_FILTER)

        # path will be None if user cancelled getOpenFileName
        if path:
            path = Path(path)

            # Take a copy of the metadata
            items = self.document.items

            if not self.close_document():
                # User does not want to close the existing document
                pass
            else:
                self.new_document(path, default_metadata_items=items)

    def _accept_drag_drop(self, event):
        """If event refers to a single file that can opened, returns the path.
        Returns None otherwise.
        """
        urls = event.mimeData().urls() if event.mimeData() else None
        path = Path(urls[0].toLocalFile()) if urls and 1 == len(urls) else None
        if path and (InselectDocument.EXTENSION == path.suffix or
                     IMAGE_SUFFIXES_RE.match(path.name)):
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

    def sync_ui(self):
        """Synchronise the user interface with the application state
        """
        document = self.document is not None
        has_rows = self.model.rowCount() > 0 if self.model else False
        boxes_view_visible = self.boxes_view == self.tabs.currentWidget()
        objects_view_visible = self.view_object == self.tabs.currentWidget()
        has_selection = len(self.view_object.selectedIndexes()) > 0

        # File
        self.copy_to_new_document_action.setEnabled(document)
        self.save_action.setEnabled(document)
        self.save_crops_action.setEnabled(has_rows)
        self.export_csv_action.setEnabled(has_rows)
        self.close_action.setEnabled(document)

        # Edit
        self.select_all_action.setEnabled(has_rows)
        self.select_none_action.setEnabled(document)
        self.next_box_action.setEnabled(has_rows)
        self.previous_box_action.setEnabled(has_rows)
        self.select_by_size_larger_action.setEnabled(has_rows)
        self.select_by_size_smaller_action.setEnabled(has_rows)
        self.delete_action.setEnabled(has_selection)
        self.rotate_clockwise_action.setEnabled(has_selection)
        self.rotate_counter_clockwise_action.setEnabled(has_selection)
        self.cookie_cutter_widget.sync_actions(document, has_rows)
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
        self.show_object_grid_action.setEnabled(objects_view_visible)
        self.show_object_expanded_action.setEnabled(objects_view_visible)
        current_colour_scheme = colour_scheme_choice().current['Name']
        for action in self.colour_scheme_actions:
            action.setChecked(current_colour_scheme == action.text())
