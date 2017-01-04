# -*- coding: utf8 -*-
"""About box
"""
import platform

import humanize
import psutil

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QDialog, QLabel, QPushButton, QSizePolicy,
                             QVBoxLayout)

from inselect.gui.utils import HTML_LINK_TEMPLATE


# Warning: lazy load of cv2 and numpy via local imports


def _environment():
    """Returns a formatted string containing version numbers of important
    dependencies
    """
    import cv2
    import numpy as np
    import scipy
    import sklearn

    # Bit depth of interpreter
    python_bit_depth = platform.architecture()[0]
    if '32bit' == python_bit_depth:
        python_bit_depth = '32 bit'
    elif '64bit' == python_bit_depth:
        python_bit_depth = '64 bit'
    else:
        python_bit_depth = ''

    versions = [
        ('Machine', _machine_summary()),
        ('Python', '{0} ({1})'.format(platform.python_version(), python_bit_depth)),
        ('Numpy', np.version.version),
        ('OpenCV', cv2.__version__),
        ('PyQt5', QtCore.PYQT_VERSION_STR),
        ('Qt',  QtCore.qVersion()),
        ('scikit-learn', sklearn.__version__),
        ('SciPy', scipy.__version__),
    ]

    return '\n'.join(['{0} {1}<br/>'.format(i, v) for i, v in versions])


def _machine_summary():
    """Returns a formatted string containing summary information about the
    machine
    """

    # Name, version and bit depth of OS
    # Mac OS X is a little fiddly - the version number in the string returned
    # by platform.platform() is the version number of the Darwin Kernel, which
    # will be different to the version of OS X.
    if 'Darwin' == platform.system():
        os_name = 'OS X {0}'.format(platform.mac_ver()[0])
    else:
        os_name = platform.platform(terse=False, aliased=True)

    if platform.machine().endswith('64'):
        os_bit_depth = '64 bit'
    else:
        # TODO Check on win32
        os_bit_depth = '32 bit'

    os = '{0} ({1})'.format(os_name, os_bit_depth)

    # Total RAM
    ram = humanize.filesize.naturalsize(psutil.virtual_memory().total, binary=True)

    return '{os}, {ram} RAM'.format(os=os, ram=ram)


def show_about_box(parent=None):
    """Shows a modal about box
    """
    body = """<h1>{application} {version}</h1>

       <p>
         Segmentation, validation and annotation of images of museum objects.

         See the <a href="https://naturalhistorymuseum.github.io/inselect/">
           {application} home page
          </a> for documentation and news. The source code is hosted in a
         <a href="https://github.com/NaturalHistoryMuseum/inselect/">
            github
         </a> repo.
         Please use our
         <a href="https://github.com/NaturalHistoryMuseum/inselect/issues">
           issues page
         </a>
         to report problems and provide suggestions.
       </p>

       <p>
         Copyright (c) 2014-2017, The Trustees of the Natural History
         Museum, London and licensed under the
         <a href="https://github.com/NaturalHistoryMuseum/inselect/blob/master/LICENSE.md">
           Modified BSD License
         </a>.
         {application} was developed by Alice Heaton, Lawrence Hudson, Pieter
         Holtzhausen and Stéfan van der Walt.
       </p>

       <h2>Acknowledgements</h2>
       <p>
        This research received support from the SYNTHESYS Project,
        <a href="http://www.synthesys.info/">www.synthesys.info</a>,
        which is financed by European Community Research Infrastructure Action
        under the FP7 Integrating Activities Programme (Grant agreement number
        312253), and from the U.K. Natural Environment Research Council.
       </p>

       <h2>Environment</h2>
       <p>
         {environment}
       </p>
    """

    # TODO LH Button to copy to clipboard
    body = body.format(
        application=QtWidgets.qApp.applicationName(),
        version=QtWidgets.qApp.applicationVersion(),
        environment=_environment()
    )
    box = QDialog(parent)
    box.setWindowTitle('About {0}'.format(QtWidgets.qApp.applicationName()))

    vlayout = QVBoxLayout()

    label = QLabel(HTML_LINK_TEMPLATE.format(body))
    label.setWordWrap(True)
    label.setTextFormat(Qt.RichText)
    label.setTextInteractionFlags(Qt.TextBrowserInteraction)
    label.setOpenExternalLinks(True)
    vlayout.addWidget(label)

    close = QPushButton('OK')
    close.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    close.setDefault(True)
    close.clicked.connect(box.close)
    vlayout.addWidget(close, alignment=QtCore.Qt.AlignHCenter)

    box.setLayout(vlayout)

    box.exec_()
