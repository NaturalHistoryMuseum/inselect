"""Freezes icons listed in icons.qrc into inselect\gui\icons.py

On Windows, this tool expects PySide-rcc.exe to be within the PySide directory,
which, at the time of writing, is where Anaconda on Windows installs it.
On other OSes, this tool expects pyside-rcc' to be on the path.

On OS X and Linux, the freeze could be implemented in bash simply as:

    pyside-rcc icons.qrc > inselect/gui/icons.py
"""
import subprocess
import sys

from pathlib import Path

if 'win32' == sys.platform:
    # PySide-rcc is tucked away on Windows and is not on the path
    import PySide
    rcc = Path(PySide.__file__).parent.joinpath('PySide-rcc.exe')
else:
    rcc = 'pyside-rcc'

with Path('inselect/gui/icons.py').open('w') as outfile:
    subprocess.call([str(rcc), 'icons.qrc'], stdout=outfile)
