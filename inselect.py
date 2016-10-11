#!/usr/bin/env python2
import sys

if sys.platform == 'win32' and hasattr(sys, 'frozen'):
    from multiprocessing import freeze_support
    freeze_support()

    # Patch DLL path so that DLL dependencies of .pyd files in subdirectories
    # can be found. Shouldn't need to do this.
    from ctypes import windll
    from pathlib import Path
    windll.kernel32.SetDllDirectoryW(unicode(Path(sys.executable).parent))


def main():
    from inselect import app
    app.main()


if __name__ == "__main__":
    main()
