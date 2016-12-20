"""Fixes for frozen binaries on Windows
"""
import sys


def fix_frozen():
    if sys.platform == 'win32' and hasattr(sys, 'frozen'):
        """Fixes for frozen binaries on Windows
        """
        # Patch DLL path so that DLL dependencies of .pyd files in
        # subdirectories can be found. Shouldn't need to do this.
        from ctypes import windll
        from pathlib import Path
        windll.kernel32.SetDllDirectoryW(str(Path(sys.executable).parent))

        # gencache does not realise that it is frozen and will not have write
        # access to the dicts.dat file. These hacks are to prevent gencache
        # from atempting to write to dicts.dat.
        # Evil, evil, evil
        import win32com.client.gencache
        win32com.client.gencache.is_readonly = True
        win32com.client.gencache.AddModuleToCache.__defaults__ = (1, False)
