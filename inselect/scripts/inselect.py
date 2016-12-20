"""Runs the application gui
"""
from multiprocessing import freeze_support

from inselect.lib.fix_frozen import fix_frozen

# The DLL path must be fixed before the app is imported
fix_frozen()

# Only has effect if running frozen on Windows
freeze_support()

if __name__ in ('__main__', 'inselect__main__'):
    # The app can be imported only once the DLL path has been patched on Windows
    from inselect.gui import app
    app.main()
