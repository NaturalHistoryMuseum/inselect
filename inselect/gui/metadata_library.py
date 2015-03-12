from PySide.QtCore import QSettings

from inselect.lib.metadata_library import library

class MetadataLibrary(object):
    """Presents library of metadata templates and maintains the current choice
    """
    def __init__(self):
        # A list of MetadataTemplate instances
        self.library = library()

        # A mapping from name to MetadataTemplate instance
        self.mapping = {t.name: t for t in self.library}

        current = QSettings().value('metadata/current_template')

        if current in self.mapping:
            self.current = self.mapping[current]
        else:
            self.current = self.mapping['Simple Darwin Core terms']

    def set_current(self, name):
        assert name in self.mapping
        self.current = self.mapping[name]
        QSettings().setValue('metadata/last_template', self.current)
        return self.current

metadata_library = MetadataLibrary()
