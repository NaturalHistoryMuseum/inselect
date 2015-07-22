from pathlib import Path

from PySide.QtCore import QObject, QSettings, Signal

from inselect.lib.templates.dwc import DWC
from inselect.lib.user_template import UserTemplate
from inselect.lib.utils import debug_print


class UserTemplateChoice(QObject):
    "Maintains the user's choice of UserTemplate"

    KEY = 'user_template_path'

    # Emitted when the user picks a new template
    template_changed = Signal()

    def __init__(self):
        super(UserTemplateChoice, self).__init__()
        self._current = DWC
        previous = QSettings().value(self.KEY)
        if previous:
            try:
                self._current = self._load(previous)
            except Exception:
                debug_print(u'Error loading user template [{0}]'.format(previous))

    def _load(sef, path):
        "Loads the UserTemplate in path"
        debug_print('UserTemplateChoice._load [{0}]'.format(path))
        with Path(path).open(encoding='utf8') as infile:
            return UserTemplate.from_file(infile)

    def load(self, path):
        "Loads the UserTemplate in path"
        debug_print('UserTemplateChoice.load [{0}]'.format(path))
        self._current = self._load(path)
        QSettings().setValue(self.KEY, str(path))
        self.template_changed.emit()

    def select_default(self):
        "Selects the default Darwin Core Archive template"
        debug_print('UserTemplateChoice.select_default'.format())
        self._current = DWC
        QSettings().setValue(self.KEY, '')
        self.template_changed.emit()

    @property
    def current(self):
        "The selected UserTemplate"
        return self._current


# Global - set to instance of UserTemplateChoice in user_template_choice
_user_template_choice = None


def user_template_choice():
    "Returns an instance of UserTemplateChoice"
    global _user_template_choice
    if not _user_template_choice:
        _user_template_choice = UserTemplateChoice()
    return _user_template_choice
