from PySide import QtGui
from PySide.QtCore import QModelIndex, Qt, QRect, QRectF
from PySide.QtGui import (QAbstractItemView, QGroupBox, QPainter, QPen,
                          QSizePolicy, QVBoxLayout, QWidget)

from .popup_panel import PopupPanel
from .roles import PixmapRole


class NavigatorView(QAbstractItemView):
    """View that provides a thumbnail navigator image of the document
    """
    SIZE = 200

    def __init__(self, parent=None, nav_toolbar=None):
        # This view is not visible
        super(NavigatorView, self).__init__(None)

        self.thumbnail = ThumbnailWidget()
        self.thumbnail.setFixedWidth(self.SIZE)
        self.thumbnail.setFixedHeight(self.SIZE)
        self.thumbnail.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.thumbnail.setContentsMargins(
            0,  # left
            0,  # top
            0,  # right
            0   # bottom
        )

        # Widget containing nav toolbar and thumbnail
        layout = QVBoxLayout()
        layout.addWidget(nav_toolbar)
        layout.addWidget(self.thumbnail)
        layout.setAlignment(self.thumbnail, Qt.AlignHCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(
            0,  # left
            0,  # top
            0,  # right
            0   # bottom
        )
        container = QWidget()
        container.setLayout(layout)

        # Widget containing toggle label and container
        self.widget = PopupPanel('Navigator', container, parent)

    def reset(self):
        """QAbstractItemView virtual
        """
        self.thumbnail.set_pixmap(self.model().data(QModelIndex(), PixmapRole))


class ThumbnailWidget(QWidget):
    def __init__(self, parent=None):
        super(ThumbnailWidget, self).__init__(parent)
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
        else:
            painter.setBrush(QtGui.qApp.palette().brush(self.backgroundRole()))
            painter.drawRect(self.rect())
