from PySide.QtCore import Qt
from PySide.QtGui import (QAction, QFileDialog, QFontMetrics, QHBoxLayout,
                          QMenu, QPushButton, QWidget)

from inselect.lib.cookie_cutter import CookieCutter
from inselect.lib.utils import debug_print

from .cookie_cutter_choice import cookie_cutter_choice
from .utils import report_to_user


class CookieCutterWidget(QWidget):
    "CookieCutter UI"

    FILE_FILTER = u'Inselect cookie cutter (*{0})'.format(
        CookieCutter.EXTENSION
    )

    def __init__(self, parent=None):
        super(CookieCutterWidget, self).__init__(parent)

        # Configure the UI
        self._create_actions()
        self.button = QPushButton("Choose cookie cutter")
        self.button.setMaximumWidth(250)
        self.button.setStyleSheet("text-align: left")
        self.popup = QMenu()
        self.inject_actions(self.popup)
        self.button.setMenu(self.popup)

        layout = QHBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)

    def _create_actions(self):
        self.save_to_new_action = QAction(
            "Save boxes to new cookie cutter...", self
        )
        self.choose_action = QAction(
            "Choose...", self, triggered=self.choose
        )
        self.clear_action = QAction(
            "Do not use a cookie cutter", self, triggered=self.clear
        )
        self.apply_current_action = QAction("Apply", self)

    def inject_actions(self, menu):
        "Adds cookie cutter actions to menu"
        menu.addAction(self.choose_action)
        menu.addAction(self.apply_current_action)
        menu.addSeparator()
        menu.addAction(self.clear_action)
        menu.addSeparator()
        menu.addAction(self.save_to_new_action)

    @report_to_user
    def clear(self):
        "Clears the choice of cookie cutter"
        cookie_cutter_choice().clear()

    @report_to_user
    def choose(self):
        "Shows a 'choose cookie cutter' file dialog"
        debug_print('CookieCutterWidget.choose_cookie_cutter')
        path, selectedFilter = QFileDialog.getOpenFileName(
            self, "Choose cookie cutter",
            unicode(cookie_cutter_choice().last_directory()),
            self.FILE_FILTER
        )

        if path:
            # Save the user's choice
            cookie_cutter_choice().load(path)

    def sync_actions(self, has_document, has_rows):
        "Sync state of actions"
        debug_print('CookieCutterWidget.sync_ui')
        current = cookie_cutter_choice().current
        has_current = cookie_cutter_choice().current is not None
        name = current.name if current else 'Choose cookie cutter'

        # Truncate text to fit button
        metrics = QFontMetrics(self.button.font())
        elided = metrics.elidedText(
            name, Qt.ElideRight, self.button.width() - 25
        )
        self.button.setText(elided)

        self.save_to_new_action.setEnabled(has_rows)
        self.clear_action.setEnabled(has_current)
        self.apply_current_action.setEnabled(has_document and has_current)
