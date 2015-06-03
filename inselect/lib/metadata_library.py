import importlib
import pkgutil

from collections import OrderedDict

from inselect.lib.metadata import MetadataTemplate
from inselect.lib.utils import debug_print

from inselect.lib.templates import (dwc, free_text, price_plecoptera,
        price_ephemeroptera, percy_cinara, percy_macrosiphoniella,
        percy_macrosiphum, percy_other_aphididae, percy_uroleucon)


if True:
    # TODO Check that template names are unique
    _library = {}
    modules = (dwc, free_text, price_plecoptera, price_ephemeroptera,
               percy_cinara, percy_macrosiphoniella, percy_macrosiphum,
               percy_other_aphididae, percy_uroleucon)
    for template in (m.template for m in modules):
        _library[template.name] = template
    _library = OrderedDict(sorted(_library.iteritems()))

    def library():
        return _library
else:
    # More flexible solution that breaks with frozen build on OS X using
    # PyInstaller

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
        # that is an instance of MetadataTemplate.
        # Returns an instance of OrderedDict with items sorted by key.
        templates = importlib.import_module('inselect.lib.templates')
        library = {}
        for loader, name, is_pkg in pkgutil.iter_modules(templates.__path__):
            try:
                pkg = importlib.import_module('{0}.{1}'.format(templates.__name__, name))
            except ImportError,e:
                debug_print(u'Error importing [{0}]: [{1}]'.format(name, e))
            else:
                template = getattr(pkg, 'template', None)
                if isinstance(template, MetadataTemplate):
                    debug_print('Loaded MetadataTemplate from [{0}]'.format(name))
                    # TODO Raise if duplicated name
                    library[template.name] = template
                else:
                    msg = u'Not an instance of MetadataTemplate [{0}]'
                    debug_print(msg.format(name))

        return OrderedDict(sorted(library.iteritems()))
