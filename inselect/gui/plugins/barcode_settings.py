from PySide.QtCore import QSettings

from inselect.lib.inselect_error import InselectError
from inselect.lib.utils import debug_print

# Warning: lazy load of gouda via local imports


def inlite_available():
    "Returns True if the Inlite engine is available"
    try:
        from gouda.engines import InliteEngine
    except ImportError:
        return False
    else:
        return InliteEngine.available()


def libdmtx_available():
    "Returns True if the libdmtx engine is available"
    try:
        from gouda.engines import LibDMTXEngine
    except ImportError:
        return False
    else:
        return LibDMTXEngine.available()


def zbar_available():
    "Returns True if the zbar engine is available"
    try:
        from gouda.engines import ZbarEngine
    except ImportError:
        return False
    else:
        return ZbarEngine.available()


def current_settings():
    """Returns a dict of the current settings:
    {
        "engine": one of ('libdmtx', 'zbar', 'inlite'),
        "inlite-format": one of ('1d', 'datamatrix', 'pdf417', 'qrcode'),
    }
    """
    s = QSettings()
    return {
        'engine': s.value('barcode/engine', 'libdmtx'),
        'inlite-format': s.value('barcode/inlite-format', 'datamatrix')
    }


def update_settings(new_settings):
    """Updates settings. new_settings should be a dict:
    {
        "engine": one of ('libdmtx', 'zbar', 'inlite'),
        "inlite-format": one of ('1d', 'datamatrix', 'pdf417', 'qrcode'),
    }
    """
    debug_print('New barcode settings', new_settings)
    s = QSettings()
    s.setValue('barcode/engine', new_settings['engine'])
    s.setValue('barcode/inlite-format', new_settings['inlite-format'])


def load_engine():
    """Returns an instance of the user's choice of barcode reading engine
    """
    try:
        from gouda.engines import InliteEngine, LibDMTXEngine, ZbarEngine
    except ImportError:
        raise InselectError('Barcode decoding is not available')
    else:
        settings = current_settings()
        engine = settings['engine']
        if 'libdmtx' == engine:
            return LibDMTXEngine()
        elif 'zbar' == engine:
            return ZbarEngine()
        elif 'inlite' == engine:
            return InliteEngine(settings['inlite-format'])
        else:
            raise ValueError('Unrecognised barcode reader [{0}]'.format(engine))
