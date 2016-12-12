from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QSizePolicy


class SideBar(QScrollArea):
    """A scrollable container for PopupPanels
    """

    def __init__(self, parent=None):
        super(SideBar, self).__init__(parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Make the controls fill the available horizontal space
        # http://qt-project.org/forums/viewthread/11012
        self.setWidgetResizable(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, 0, 0, 0)

    def resizeEvent(self, event):
        """Virtual
        """
        self.setViewportMargins(0, 0, 0, 0)
        return super(SideBar, self).resizeEvent(event)
