from __future__ import print_function, division

import argparse
import sys

from PySide import QtCore, QtGui

import inselect

from inselect.lib.utils import debug_print
from inselect.gui.app import MainWindow


def main():
    parser = argparse.ArgumentParser(description='Runs the inselect user-interface')
    parser.add_argument("file", help='The inselect document to open', nargs='?')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Show debug messages')
    parser.add_argument('-l', '--locale', action='store',
                        help='Use LOCALE; intended for testing purposes only')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + inselect.__version__)
    args = parser.parse_args()

    inselect.lib.utils.DEBUG_PRINT = args.debug

    app = QtGui.QApplication(sys.argv)

    # The QSettings default constructor uses the application's organizationName
    # and applicationName properties.
    app.setOrganizationName('NHM')
    app.setApplicationName('inselect')

    debug_print(u'Settings stored in [{0}]'.format(QtCore.QSettings().fileName()))

    # No obvious benefit to also setting the version but neither is there any
    # obvious harm
    app.setApplicationVersion(inselect.__version__)

    if args.locale:
        debug_print('Will set locale to [{0}]'.format(args.locale))
        QtCore.QLocale.setDefault(QtCore.QLocale(args.locale))

    debug_print(u'Locale is [{0}]'.format(QtCore.QLocale().name()))

    window = MainWindow(app)
    window.show_from_geometry_settings()

    if args.file:
        window.open_file(args.file)

    sys.exit(app.exec_())
