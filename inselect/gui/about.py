"""About box
"""
import platform

import cv2
import humanize
import numpy as np
import psutil
import PySide
import PySide.QtCore

from PySide import QtGui
from PySide.QtGui import QMessageBox


def _environment():
    """Returns a formatted string containing version numbers of important
    dependencies
    """
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
        ('PySide', PySide.__version__),
        ('Qt', PySide.QtCore.__version__),  # Version compiled against
    ]

    return '\n'.join(['<p>{0}: {1}</p>'.format(i, v) for i, v in versions])


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
    """Shows a model about box
    """
    text = u"""<h1>{application} {version}</h1>

       <p>
         Segmentation, validation and annotation of images of museum objects.
         Please use our
         <a href="https://github.com/NaturalHistoryMuseum/inselect">
           issues page
         </a>
         to report problems and provide suggestions.
       </p>

       Inselect is Copyright (c) 2014-2016, The Trustees of the Natural History
       Museum, London and licensed under the
       <a href="https://github.com/NaturalHistoryMuseum/inselect/blob/master/LICENSE.md">
         Modified BSD License
       </a>.

       <h2>Acknowledgements</h2>
       <p>
        This research received support from the SYNTHESYS Project,
        <a href="http://www.synthesys.info/">www.synthesys.info</a>,
        which is financed by European Community Research Infrastructure Action
        under the FP7 Integrating Activities Programme (Grant agreement number
        312253), and from the U.K. Natural Environment Research Council.
       </p>

       <h2>Contributors</h2>
       <p>
           <strong>Alice Heaton</strong>: Application development
       </p>
       <p>
           <strong>Lawrence Hudson</strong>: Application development
       </p>
       <p>
           <strong>Pieter Holtzhausen</strong>: Application development
           and segmentation algorithm
       </p>
       <p>
           <strong>Stefan van der Walt</strong>: Application development
           and segmentation algorithm
       </p>

       <h2>Environment</h2>
       {environment}
    """

    # TODO LH Button to copy to clipboard
    text = text.format(application=QtGui.qApp.applicationName(),
                       version=QtGui.qApp.applicationVersion(),
                       environment=_environment())
    QMessageBox.about(parent, 'About {0}'.format(QtGui.qApp.applicationName()),
                      text)
