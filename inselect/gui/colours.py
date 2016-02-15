from PySide.QtCore import QObject, QSettings, Signal
from PySide.QtGui import QColor


LIGHT_BACKGROUND = {
    'Name': 'Light background',
    'Description': 'Works well with objects that are on a light background',
    'Colours': {
        'Valid':        QColor(0x00, 0x00, 0xff),
        'Invalid':      QColor(0x00, 0x00, 0xff),
        'InvalidFill':  QColor(0xfb, 0x9a, 0x99, 0x50),
        'Selected':     QColor(0xfb, 0x00, 0x00),
        'Resizing':     QColor(0xfb, 0x00, 0x00, 0x50),
        'GridInvalid':  QColor(0xfb, 0x9a, 0x99),
    }
}

DARK_BACKGROUND = {
    'Name': 'Dark background',
    'Description': 'Works well with objects that are on a dark background',
    'Colours': {
        'Valid':        QColor(0x28, 0xdb, 0xf2),
        'Invalid':      QColor(0x28, 0xdb, 0xf2),
        'InvalidFill':  QColor(0xfb, 0x9a, 0x99, 0x50),
        'Selected':     QColor(0xc2, 0x44, 0x4e),
        'Resizing':     QColor(0xa9, 0x2f, 0x41, 0xa0),
        'GridInvalid':  QColor(0xfb, 0x9a, 0x99),
    }
}


COLOURS = {v['Name']: v for v in (LIGHT_BACKGROUND, DARK_BACKGROUND)}


class ColourSchemeChoice(QObject):
    """User's choice of color scheme
    """
    # Mapping from name to colour dict

    KEY = 'colour_scheme'

    # Emitted when the user picks a new colour scheme
    colour_scheme_changed = Signal()

    def __init__(self):
        super(ColourSchemeChoice, self).__init__()
        self._current = DARK_BACKGROUND
        previous = QSettings().value(self.KEY)
        if previous and previous in COLOURS:
            self._current = COLOURS[previous]

    def colour_scheme_names(self):
        "A list of names of colour schemes"
        return sorted(COLOURS.keys())

    def set_colour_scheme(self, name):
        "Sets the colour scheme"
        if name not in COLOURS:
            raise ValueError('[{0}] is not the name of a colour scheme'.format(name))
        else:
            QSettings().setValue(self.KEY, name)
            self._current = COLOURS[name]
            self.colour_scheme_changed.emit()

    @property
    def current(self):
        "The selected colour scheme, a dict"
        return self._current

# Global - set to instance of ColourSchemeChoice in colour_scheme_choice
_colour_scheme_choice = None


def colour_scheme_choice():
    "Returns an instance of ColourSchemeChoice"
    global _colour_scheme_choice
    if not _colour_scheme_choice:
        _colour_scheme_choice = ColourSchemeChoice()
    return _colour_scheme_choice
