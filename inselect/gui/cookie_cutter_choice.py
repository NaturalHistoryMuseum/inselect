from pathlib import Path

from PySide.QtCore import QObject, QSettings, Signal
from PySide.QtGui import QDesktopServices

from inselect.lib.cookie_cutter import CookieCutter
from inselect.lib.utils import debug_print


# Global - set to instance of CookieCutterChoice in cookie_cutter_boxes
_COOKIE_CUTTER_CHOICE = None


def cookie_cutter_choice():
    "Returns an instance of CookieCutterChoice"
    global _COOKIE_CUTTER_CHOICE
    if not _COOKIE_CUTTER_CHOICE:
        _COOKIE_CUTTER_CHOICE = CookieCutterChoice()
    return _COOKIE_CUTTER_CHOICE


class CookieCutterChoice(QObject):
    "Maintains the user's choice of CookieCutter"

    PATH_KEY = 'cookie_cutter_path'
    DIRECTORY_KEY = 'cookie_cutter_last_directory'

    # Emitted when the user picks a new file
    cookie_cutter_changed = Signal()

    def __init__(self):
        super(CookieCutterChoice, self).__init__()
        self._current = None
        previous = QSettings().value(self.PATH_KEY)
        if previous:
            try:
                self._current = self._load(previous)
            except Exception:
                debug_print(
                    u'Error loading cookie cutter [{0}]'.format(previous)
                )

    @classmethod
    def last_directory(cls):
        "Path the the most recently used directory"
        return Path(QSettings().value(
            cls.DIRECTORY_KEY,
            QDesktopServices.storageLocation(QDesktopServices.DocumentsLocation)
        ))

    def _load(self, path):
        "Loads the CookieCutter in path"
        debug_print(u'CookieCutterChoice._load [{0}]'.format(path))
        return CookieCutter.load(path)

    def load(self, path):
        """Loads the CookieCutter in path, updates settings and emits
        cookie_cutter_changed
        """
        debug_print(u'CookieCutterChoice.load [{0}]'.format(path))
        self._current = self._load(path)
        QSettings().setValue(self.PATH_KEY, unicode(path))
        QSettings().setValue(self.DIRECTORY_KEY, unicode(Path(path).parent))
        self.cookie_cutter_changed.emit()

    def clear(self):
        "Selects cookie cutter"
        debug_print('CookieCutterChoice.clear')
        self._current = None
        QSettings().setValue(self.PATH_KEY, '')
        self.cookie_cutter_changed.emit()

    def create_and_use(self, boxes, path):
        """Creates a new CookieCutter file that contains boxes, writes in to
        path and sets it to be the current choice
        """
        debug_print(u'CookieCutterChoice.create_and_use to [{0}]'.format(path))
        cookie_cutter = CookieCutter('', boxes)
        cookie_cutter.save(path)
        self.load(path)

    @property
    def current(self):
        "The selected CookieCutter"
        return self._current
