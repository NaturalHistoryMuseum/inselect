import argparse
import locale
import re
import sys

from pathlib import Path

from qtpy import QtWidgets
from qtpy.QtCore import QCoreApplication, QLocale, QSettings, QSize, QTimer
from qtpy.QtGui import QIcon

import inselect

from .lib.utils import debug_print
from .gui.main_window import MainWindow
from .gui.utils import report_exception_to_user


# Values used by several important parts of Qt's machinery including the GUI
# and QSettings.
QCoreApplication.setOrganizationName('NHM')
QCoreApplication.setApplicationName('Inselect')
QCoreApplication.setApplicationVersion(inselect.__version__)
QCoreApplication.setOrganizationDomain('nhm.ac.uk')

APP = None


def qapplication(args=None):
    "Returns the QApplication for this instance"
    global APP
    if not APP:
        APP = QtWidgets.qApp = QtWidgets.QApplication(args if args else [])
    return APP


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description='Runs the inselect user-interface'
    )
    parser.add_argument(
        "file", help='The inselect document to open', nargs='?', type=Path
    )
    parser.add_argument(
        '-d', '--debug', action='store_true', help='Show debug messages'
    )
    parser.add_argument(
        '-l', '--locale', action='store',
        help='Use LOCALE; intended for dev purposes only'
    )
    parser.add_argument(
        '-q', '--quit', action='store_true',
        help='Exit immediately after showing the main window; intended for dev '
             'purposes only'
    )
    parser.add_argument(
        '-s', '--stylesheet', action='store', type=Path,
        help='Use stylesheet; intended for dev purposes only'
    )
    parser.add_argument(
        '-t', '--print-time', action='store_true',
        help='Will print, when a document is closed, the elapsed time for '
             'which the document was open'
    )
    parser.add_argument(
        '-v', '--version', action='version',
        version='%(prog)s ' + inselect.__version__
    )
    parser.add_argument(
        '-w', '--window-size', action='store', type=_window_size,
        help='Set window size to WxH'
    )
    parsed = parser.parse_args(args)

    # TODO LH A command-line switch to clear all QSettings

    inselect.lib.utils.DEBUG_PRINT = parsed.debug

    # Only one instance of QApplication can be created per process. The single
    # instance is stored in QtWidgets.qApp. When test plans are being run it is
    # likely that the QApplication will have been created by a unittest.
    QtWidgets.qApp = qapplication(args)

    # Install global exception hook only after the application has been created
    sys.excepthook = report_exception_to_user

    debug_print('Settings stored in [{0}]'.format(QSettings().fileName()))

    if parsed.locale:
        debug_print('Will set locale to [{0}]'.format(parsed.locale))
        QLocale.setDefault(QLocale(parsed.locale))
        locale.setlocale(locale.LC_ALL, parsed.locale)
    else:
        # Set Python's locale module to the user's default locale
        locale.setlocale(locale.LC_ALL, '')

    debug_print('Locale is [{0}]'.format(QLocale().name()))

    # Application icon
    icon = QIcon()
    path = ':/icons/inselect{0}.png'
    for size in (16, 24, 32, 48, 64, 128, 256, 512):
        icon.addFile(path.format(size), QSize(size, size))
    QtWidgets.qApp.setWindowIcon(icon)

    # Stylesheet
    QtWidgets.qApp.setStyleSheet(_stylesheet(parsed.stylesheet))

    # Create and show main windows
    window = MainWindow(parsed.print_time)
    if parsed.window_size:
        window.show_with_size(parsed.window_size)
    else:
        window.show_from_geometry_settings()

    if parsed.file:
        # Process messages before loading document
        QtWidgets.qApp.processEvents()
        window.open_file(parsed.file)

    if parsed.quit:
        sys.exit(0)
    else:
        QTimer.singleShot(100, window.show_shortcuts_post_startup)
        sys.exit(QtWidgets.qApp.exec_())


def _stylesheet(user_stylesheet):
    if user_stylesheet:
        path = user_stylesheet
    else:
        if hasattr(sys, 'frozen'):
            root = Path(sys.executable).parent
        else:
            root = Path(__file__).parent
        path = root.joinpath('inselect.qss')

    with path.open() as infile:
        return infile.read()


def _window_size(v):
    """Raises argparse.ArgumentTypeError() if v is not a string in the format
    WxH, where W and H are integers greater than zero. Otherwise returns a QSize
    of W and H.
    """
    match = re.match("^([0-9]+)x([0-9]+)$", v)
    if match:
        w, h = match.groups()
        return QSize(int(w), int(h))
    else:
        raise argparse.ArgumentTypeError("Should be in the form 'WxH'")
