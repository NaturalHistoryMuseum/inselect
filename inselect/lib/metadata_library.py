import importlib
import pkgutil
import sys

from inselect.lib.metadata import MetadataTemplate
from inselect.lib.utils import debug_print

_library = None


def library():
    """Returns a list of MetadataTemplate instances
    """
    global _library
    if not _library:
        _library = _load_library()
    return _library

def _load_library():
    # Import everything inselect.lib.templates that has a 'template' name
    # that is an instance of MetadataTemplate
    try:
        templates = importlib.import_module('.lib.templates', 'inselect')
    except ImportError,e:
        debug_print(e)
    else:
        library = []
        for loader, name, is_pkg in pkgutil.iter_modules(templates.__path__):
            try:
                pkg = importlib.import_module('{0}.{1}'.format(templates.__name__, name))
            except ImportError,e:
                debug_print(u'Error importing [{0}]: [{1}]'.format(name, e))
            else:
                template = getattr(pkg, 'template', None)
                if isinstance(template, MetadataTemplate):
                    debug_print('Loaded MetadataTemplate from [{0}]'.format(name))
                    library.append(template)
                else:
                    msg = u'Not an instance of MetadataTemplate [{0}]'
                    debug_print(msg.format(name))
        return library
