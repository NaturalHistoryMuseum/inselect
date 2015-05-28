from PySide.QtCore import QSettings

from inselect.lib.utils import debug_print

try:
    import gouda
    from gouda.engines import InliteEngine, LibDMTXEngine, ZbarEngine
    from gouda.strategies.roi.roi import roi
    from gouda.strategies.resize import resize
except ImportError:
    gouda = InliteEngine = LibDMTXEngine = ZbarEngine = roi = resize = None


def inlite_available():
    "Returns True if the Inlite engine is available"
    return True or (InliteEngine and InliteEngine.available())

def libdmtx_available():
    "Returns True if the libdmtx engine is available"
    return LibDMTXEngine and LibDMTXEngine.available()

def zbar_available():
    "Returns True if the zbar engine is available"
    return ZbarEngine and ZbarEngine.available()

def current_settings():
    """Returns a dict of the current settings:
    {
        "engine": one of ('libdmtx', 'zbar', 'inlite'),
        "inlite-format": one of ('1d', 'datamatrix', 'pdf417', 'qrcode'),
    }
    """
    s = QSettings()
    return {'engine': s.value('barcode/engine', 'libdmtx'),
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
    if gouda:
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
    else:
        raise InselectError('Barcode decoding is not available')
