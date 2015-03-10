from __future__ import print_function, division

import argparse
import sys

from PySide.QtCore import QSettings, QLocale, QCoreApplication
from PySide.QtGui import QApplication

import inselect

from inselect.lib.utils import debug_print
from inselect.gui.app import MainWindow

# The QSettings default constructor uses the application's organizationName
# and applicationName properties.
QCoreApplication.setOrganizationName('NHM')
QCoreApplication.setApplicationName('inselect')

# No obvious benefit to also setting these but neither is there any obvious harm
QCoreApplication.setApplicationVersion(inselect.__version__)
QCoreApplication.setOrganizationDomain('nhm.ac.uk')


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

    # TODO LH A command-line switch to clear all QSettings

    inselect.lib.utils.DEBUG_PRINT = args.debug

    app = QApplication(sys.argv)

    debug_print(u'Settings stored in [{0}]'.format(QSettings().fileName()))

    if args.locale:
        debug_print('Will set locale to [{0}]'.format(args.locale))
        QLocale.setDefault(QLocale(args.locale))

    debug_print(u'Locale is [{0}]'.format(QLocale().name()))

    window = MainWindow(app)
    window.show_from_geometry_settings()

    if args.file:
        window.open_file(args.file)

    sys.exit(app.exec_())
