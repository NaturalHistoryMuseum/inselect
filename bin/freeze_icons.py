"""For Windows, where the PySide-rcc tool is hidden away
"""
import subprocess
from pathlib import Path

import PySide

rcc = Path(PySide.__file__).parent.joinpath('PySide-rcc.exe')

with Path('inselect\gui\icons.py').open('w') as outfile:
    subprocess.call([str(rcc), 'icons.qrc'], stdout=outfile)
