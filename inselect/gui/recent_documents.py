from pathlib import Path

from PySide.QtCore import QSettings

from inselect.lib.utils import debug_print


class RecentDocuments(object):
    KEY = 'recent_documents'

    MAX_RECENT_DOCS = 5

    def read_paths(self):
        """Returns a list of up to MAX_RECENT_DOCS Paths. The most recently
        opened path is the first element in the list.
        """
        settings = QSettings()
        n_recent = settings.beginReadArray(self.KEY)
        try:
            n_recent = min(n_recent, self.MAX_RECENT_DOCS)
            recent = [None] * n_recent
            debug_print('Reading {0} recent documents path'.format(n_recent))
            for index in xrange(n_recent):
                settings.setArrayIndex(index)
                path = settings.value("path")
                recent[index] = self._resolved_if_possible(Path(path))
        finally:
            settings.endArray()

        return recent

    def add_path(self, path):
        "Adds path to recent documents"
        recent = self.read_paths()

        # Make the path absolute, resolving any symlinks.
        path = self._resolved_if_possible(Path(path))

        # Remove the existing occurrence of path, if present.
        # A linear scan is acceptable here because the list will always
        # be very short
        try:
            recent.remove(path)
        except ValueError:
            # path is not currently in recent
            pass

        # Prepend the path
        recent.insert(0, str(path))

        # Limit to MAX_RECENT_DOCS
        recent = recent[:self.MAX_RECENT_DOCS]

        debug_print('Writing {0} recent document paths'.format(len(recent)))

        settings = QSettings()
        settings.beginWriteArray(self.KEY, len(recent))
        try:
            for index, path in enumerate(recent):
                settings.setArrayIndex(index)
                settings.setValue('path', str(path))
        finally:
            settings.endArray()

    def _resolved_if_possible(self, path):
        """Returns path made absolute, resolving any symlinks. If path cannot
        be resolved it is returned unaltered.
        """
        try:
            return path.resolve()
        except OSError:
            return path
