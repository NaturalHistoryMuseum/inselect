from __future__ import print_function, division

import argparse
import sys

from PySide import QtGui

import inselect
import inselect.settings

from inselect.gui.app import MainWindow


def main():
    parser = argparse.ArgumentParser(description='Runs the inselect user-interface')
    parser.add_argument("file", help='The inselect document to open', nargs='?')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Show debug messages')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + inselect.__version__)
    args = parser.parse_args()

    inselect.settings.init()
    inselect.lib.utils.DEBUG_PRINT = args.debug

    app = QtGui.QApplication(sys.argv)
    window = MainWindow(app)

    # TODO LH Persist window state in settings
    open_fullscreen = False
    if open_fullscreen:
        window.showFullScreen()
    else:
        desktop = QtGui.QDesktopWidget()
        window.setGeometry(0, 0, desktop.width(), desktop.height()*0.75)
        window.show()


    if args.file:
        window.open_file(args.file)

    sys.exit(app.exec_())
