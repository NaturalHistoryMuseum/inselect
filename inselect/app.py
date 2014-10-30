"""Inselect.

Usage:
    main.py [--verbose] 
    main.py [--verbose] <filename>

Options:
  -h --help             Show this screen.
  --version             Show version.
  --verbose             Print debug output.
"""
from __future__ import print_function, division

from PySide import QtGui

import sys

from docopt import docopt

import inselect
import inselect.lib.utils
import inselect.settings
from inselect.gui.app import InselectMainWindow


def launch_gui(filename=None):
    app = QtGui.QApplication(sys.argv)
    window = InselectMainWindow(app)
    if filename:
        window.open_document(filename)
    window.showMaximized()
    window.splitter.setSizes([800, 100])
    window.show()
    sys.exit(app.exec_())


def launch():
    # TODO Remove docopt and use argparse - loose a dependency and gain flexibiity
    arguments = docopt(__doc__, version='Inselect [{0}]'.format(inselect.__version__))
    inselect.settings.init()
    inselect.lib.utils.DEBUG_PRINT = arguments['--verbose']
    print("Launching gui")
    filename = arguments['<filename>']
    launch_gui(filename)
