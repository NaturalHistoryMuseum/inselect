from PySide.QtCore import QSettings

from inselect.lib.metadata_library import library
from inselect.lib.utils import debug_print

class MetadataLibrary(object):
    """Presents library of metadata templates and maintains the current choice
    """
    def __init__(self):
        # A list of MetadataTemplate instances
        self.choices = library()

        current = QSettings().value('metadata/current_template')
        debug_print('Current metadata template [{0}]'.format(current))

        if current in self.choices:
            self.current = self.choices[current]
        else:
            self.current = self.choices['Simple Darwin Core terms']

    def set_current(self, name):
        debug_print('MetadataLibrary.set_current [{0}]'.format(name))
        assert name in self.choices
        self.current = self.choices[name]
        QSettings().setValue('metadata/current_template', self.current.name)
        return self.current

_library = None


def metadata_library():
    """Returns an instance of MetadataLibrary
    """
    global _library
    if not _library:
        _library = MetadataLibrary()
    return _library
