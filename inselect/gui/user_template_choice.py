from pathlib import Path

from PyQt5.QtCore import QObject, QSettings, pyqtSignal, QStandardPaths

from inselect.lib.templates.dwc import DWC
from inselect.lib.user_template import UserTemplate
from inselect.lib.utils import debug_print


# Global - set to instance of UserTemplateChoice in user_template_choice
_USER_TEMPLATE_CHOICE = None


def user_template_choice():
    "Returns an instance of UserTemplateChoice"
    global _USER_TEMPLATE_CHOICE
    if not _USER_TEMPLATE_CHOICE:
        _USER_TEMPLATE_CHOICE = UserTemplateChoice()
    return _USER_TEMPLATE_CHOICE


class UserTemplateChoice(QObject):
    "Maintains the user's choice of UserTemplate"

    PATH_KEY = 'user_template_path'
    DIRECTORY_KEY = 'user_template_last_directory'

    DEFAULT = DWC

    # Emitted when the user picks a new template
    template_changed = pyqtSignal()

    def __init__(self):
        super(UserTemplateChoice, self).__init__()
        self._current = self.DEFAULT
        previous = QSettings().value(self.PATH_KEY)
        if previous:
            try:
                self._current = self._load(previous)
            except Exception:
                debug_print('Error loading user template [{0}]'.format(previous))

    @classmethod
    def last_directory(cls):
        "Path the the most recently used directory"
        return Path(QSettings().value(
            cls.DIRECTORY_KEY,
            QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        ))

    def _load(self, path):
        "Loads the UserTemplate in path"
        debug_print('UserTemplateChoice._load [{0}]'.format(path))
        return UserTemplate.load(path)

    def load(self, path):
        "Loads the UserTemplate in path"
        debug_print('UserTemplateChoice.load [{0}]'.format(path))
        self._current = self._load(path)
        QSettings().setValue(self.PATH_KEY, str(path))
        QSettings().setValue(self.DIRECTORY_KEY, str(Path(path).parent))
        self.template_changed.emit()

    def select_default(self):
        "Selects the default Darwin Core Archive template"
        debug_print('UserTemplateChoice.select_default')
        self._current = self.DEFAULT
        QSettings().setValue(self.PATH_KEY, '')
        self.template_changed.emit()

    def refresh(self):
        """Reloads the current template
        """
        debug_print('UserTemplateChoice.refresh'.format())
        current = QSettings().value(self.PATH_KEY)
        if current:
            # A template to refresh
            self.load(current)
        else:
            # Using the default (DWC) template - no need to do anything
            pass

    @property
    def current_path(self):
        """The path to the selected UserTemplate or None, if the default
        template is selected
        """
        current = QSettings().value(self.PATH_KEY)
        return Path(current) if current else None

    @property
    def current(self):
        "The selected UserTemplate"
        return self._current

    @property
    def current_is_default(self):
        "True if self.current is the default template"
        return self._current == self.DEFAULT
