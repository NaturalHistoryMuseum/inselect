import sys

from pathlib import Path

from inselect.gui import app

if sys.platform == 'win32' and hasattr(sys, 'frozen'):
    from multiprocessing import freeze_support
    freeze_support()

    # Patch DLL path so that DLL dependencies of .pyd files in subdirectories
    # can be found. Shouldn't need to do this.
    from ctypes import windll
    windll.kernel32.SetDllDirectoryW(str(Path(sys.executable).parent))


if __name__ in ('__main__', 'inselect__main__'):
    app.main()
