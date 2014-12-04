"""Inselect.

Usage:
    main.py [--debug] 
    main.py [--debug] <filename>

Options:
  -h --help             Show this screen.
  --version             Show version.
  --debug               Print debug output.
"""
from __future__ import print_function, division

from PySide import QtGui

import sys

from docopt import docopt

import inselect
import inselect.lib.utils
import inselect.settings
from inselect.gui.app import MainWindow


def launch_gui(filename=None):
    app = QtGui.QApplication(sys.argv)
    window = MainWindow(app)
    open_fullscreen = False
    if open_fullscreen:
        window.showFullScreen()
    else:
        desktop = QtGui.QDesktopWidget()
        window.setGeometry(0, 0, desktop.width(), desktop.height()*0.75)
        window.show()

    if filename:
        window.open_document(filename)
    sys.exit(app.exec_())


def launch():
    # TODO Remove docopt and use argparse - loose a dependency and gain flexibiity
    arguments = docopt(__doc__, version='inselect {0}'.format(inselect.__version__))
    inselect.settings.init()
    inselect.lib.utils.DEBUG_PRINT = arguments['--debug']
    print("Launching gui")
    filename = arguments['<filename>']
    launch_gui(filename)
