import argparse
import sys

from PySide import QtGui
from PySide.QtCore import QSettings, QLocale, QCoreApplication

import inselect

from inselect.lib.utils import debug_print
from inselect.gui.main_window import MainWindow

# Values used by several important parts of Qt's machinery including the GUI
# and QSettings.
QCoreApplication.setOrganizationName('NHM')
QCoreApplication.setApplicationName('Inselect')
QCoreApplication.setApplicationVersion(inselect.__version__)
QCoreApplication.setOrganizationDomain('nhm.ac.uk')


def main(args):
    parser = argparse.ArgumentParser(description='Runs the inselect user-interface')
    parser.add_argument("file", help='The inselect document to open', nargs='?')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Show debug messages')
    parser.add_argument('-l', '--locale', action='store',
                        help='Use LOCALE; intended for testing purposes only')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + inselect.__version__)
    parsed = parser.parse_args(args[1:])

    # TODO LH A command-line switch to clear all QSettings

    inselect.lib.utils.DEBUG_PRINT = parsed.debug

    # Only one instance of QApplication can be created per process. The single
    # instance is stored in QtGui.qApp. When test plans are being run it is
    # likely that the QApplication will have been created by a unittest.
    app = QtGui.qApp if QtGui.qApp else QtGui.QApplication(args)

    debug_print(u'Settings stored in [{0}]'.format(QSettings().fileName()))

    if parsed.locale:
        debug_print('Will set locale to [{0}]'.format(parsed.locale))
        QLocale.setDefault(QLocale(parsed.locale))

    debug_print(u'Locale is [{0}]'.format(QLocale().name()))

    window = MainWindow(app)
    window.show_from_geometry_settings()

    if parsed.file:
        window.open_file(parsed.file)

    sys.exit(app.exec_())
