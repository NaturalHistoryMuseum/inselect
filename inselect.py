#!/usr/bin/env python
import sys
from inselect import app

if sys.platform == 'win32':
    from multiprocessing import freeze_support
    freeze_support()

app.launch()
