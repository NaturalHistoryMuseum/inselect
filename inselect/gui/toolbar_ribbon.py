from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QSizePolicy, QToolBar, QToolButton,
                             QWidget)

from .ribbon import Ribbon


class ToolbarRibbon(Ribbon):
    """A ribbon with helpers for containing toolbars
    """
    def add_toolbar(self, title=None, toolbar=None):
        """Creates, adds and returns a QToolBar
        """
        if 1 != bool(toolbar) + bool(title):
            raise ValueError('Just one of toolbar or title should be given')
        if not toolbar:
            toolbar = QToolBar(title)
        toolbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.addTab(toolbar, toolbar.windowTitle())

        # This style applies to QToolButtons that are immediate children
        # of the toolbar - it does not apply to QToolButtons that are
        # contained within QWidgets added to toolbar.
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        toolbar.setMovable(False)
        toolbar.setFloatable(False)
        return toolbar

    def create_button(self, action=None, icon=None, text=None, menu=None,
                      tooltip=None, properties={}):
        """Returns a QToolButton
        """
        button = QToolButton()
        if action:
            button.setDefaultAction(action)
        if icon:
            button.setIcon(icon)
        if text:
            button.setText(text)
        if menu:
            button.setMenu(menu)
            button.setPopupMode(QToolButton.InstantPopup)
        if tooltip:
            button.setToolTip(tooltip)
        for key, value in properties.items():
            button.setProperty(key, value)

        button.setAutoRaise(True)
        button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # Point size for text buttons
        # button.setFont(toolbar.font())

        # Expanding in x and in y so that text buttons fill available space
        button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        return button

    def create_panel(self):
        """Returns a tuple QGridLayout, ToolbarRibbonPanel for a new block of
        controls.
        """
        panel = QWidget()
        panel.setContentsMargins(0, 0, 0, 0)

        layout = QGridLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # layout.setRowMinimumHeight(2, 1)

        return layout, panel
