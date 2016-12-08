from multiprocessing import freeze_support

from inselect.lib.utils import fix_frozen_dll_path
from inselect.gui import app


if __name__ in ('__main__', 'inselect__main__'):
    # Only has effect if running frozen on Windows
    freeze_support()
    fix_frozen_dll_path()
    app.main()
