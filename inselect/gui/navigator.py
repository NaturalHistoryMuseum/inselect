from PySide.QtCore import QModelIndex, Qt, QRect, QRectF
from PySide.QtGui import (QAbstractItemView, QBrush, QColor, QPen, QPainter,
                          QVBoxLayout, QWidget)

from .popup_panel import PopupPanel
from .roles import PixmapRole


class NavigatorView(QAbstractItemView):
    """View that provides a thumbnail navigator image of the document
    """
    SIZE = 200

    def __init__(self, parent=None, nav_toolbar=None):
        # This view is not visible
        super(NavigatorView, self).__init__(None)

        self.navigator = Navigator()
        self.navigator.setFixedWidth(self.SIZE)
        self.navigator.setFixedHeight(self.SIZE)
        self.navigator.setContentsMargins(0, 0, 0, 0)

        # Widget containing nav toolbar and thumbnail
        layout = QVBoxLayout()
        if nav_toolbar:
            layout.addWidget(nav_toolbar)
        layout.addWidget(self.navigator)
        layout.setAlignment(self.navigator, Qt.AlignHCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        container = QWidget()
        container.setContentsMargins(0, 0, 0, 0)
        container.setLayout(layout)

        # Widget containing toggle label and container
        self.widget = PopupPanel('Navigator', container, parent=parent)
        self.widget.setContentsMargins(0, 0, 0, 0)

    def reset(self):
        """QAbstractItemView virtual
        """
        self.navigator.set_pixmap(self.model().data(QModelIndex(), PixmapRole))


class Navigator(QWidget):
    def __init__(self, parent=None):
        super(Navigator, self).__init__(parent)
        self.pixmap = None
        self.focus = None

    def set_pixmap(self, pixmap):
        self.pixmap = pixmap
        self.update()

    def new_focus_rect(self, focus):
        """focus - a QRectF in normalised (i.e., between 0 and 1) coordinates
        """
        self.focus = focus
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.pixmap:
            size = self.pixmap.size()
            aspect = float(size.width()) / size.height()
            if aspect > 1:
                # Image is wider than it is tall - centre vertically
                left = 0
                width = self.width()
                height = self.height() / aspect
                top = (self.height() - height) / 2
            else:
                # Image is taller than it is wide - centre horizontally
                top = 0
                height = self.height()
                width = self.width() * aspect
                left = (self.width() - width) / 2

            painter.drawPixmap(QRect(left, top, width, height), self.pixmap)

            if self.focus:
                # self.focus contains coords between 0 and 1 - translate these
                # to pixels
                pixels = QRectF(left + self.focus.left() * width,
                                top + self.focus.top() * height,
                                self.focus.width() * width,
                                self.focus.height() * height)
                # Outer box in white
                painter.setPen(QPen(Qt.white, 1, Qt.SolidLine))
                painter.drawRect(pixels)
                # Inner box in black
                painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                painter.drawRect(pixels.adjusted(1, 1, -1, -1))
