from PySide import QtGui, QtCore
from inselect.gui.box_resizable import BoxResizable


class GraphicsScene(QtGui.QGraphicsScene):
    """The GraphicsScene holds all the boxes displayed to the user.

    It handles selecting/deselecting items and generating pixmaps.

    The GraphicsScene listens for segments being added/removed to the
    segment scene, and adds/removes BoxResizable items to the scene
    correspondingly.
    """
    def __init__(self, segment_scene):
        # Constructors
        QtGui.QGraphicsScene.__init__(self)
        # Setup members
        self._segment_scene = segment_scene
        self._boxes_with_keyboard_focus = []
        self._image_item = None
        self._pixmap = None
        # Watch modifications on the segment scene
        self._segment_scene.watch('after-segment-add', self._after_segment_add)
        self._segment_scene.watch('before-segment-remove',
                                  self._before_segment_remove)

    def set_image(self, image):
        """Set the image to work from

        Parameters
        ----------
        image : QtCore.QImage
        """
        self._pixmap = QtGui.QPixmap.fromImage(image)
        if self._image_item is None:
            self._image_item = QtGui.QGraphicsPixmapItem(self._pixmap)
            self.addItem(self._image_item)
        else:
            self._image_item.setPixmap(self._pixmap)
        self.setSceneRect(0, 0, image.width(), image.height())

    def pixmap(self):
        """Return the pixmap of this scene

        Returns
        -------
        QtGui.QPixmap
        """
        return self._pixmap

    def segment_scene(self):
        """Return the segment scene associated with this graphics scene

        Returns
        -------
        SegmentScene
        """
        return self._segment_scene

    def selected_segments(self):
        """Return the currently selected segments

        Returns
        -------
        list of Segment
        """
        segments = []
        for box in self.selectedItems():
            segment = self._segment_scene.get_associated_segment(box)
            segments.append(segment)
        return segments

    def select_all_segments(self):
        """Select all segments in the scene"""
        for box in self.items():
            box.setSelected(True)

    def deselect_all_segments(self):
        """Deselect all segments in the scene"""
        for box in self.selectedItems():
            box.setSelected(False)

    def select_segment(self, segment, deselect_others=True):
        """Select the given segment.

        Parameters
        ----------
        segment : Segment
        deselect_others : bool
            If True (default) then it de-selects other segments first.
            Otherwise it adds the given segment to the list of selected
            segments.
        """
        if deselect_others:
            self.deselect_all_segments()
        box = segment.get_associated_object(BoxResizable)
        box.setSelected(True)

    def set_keyboard_focus(self, segment, focus):
        """Indiciate whether a given segment has keyboard focus

        Parameters
        ----------
        segment : Segment
        focus : bool
        """
        box = segment.get_associated_object(BoxResizable)
        box.set_keyboard_focus(focus)
        self._boxes_with_keyboard_focus.append(box)

    def remove_keyboard_focus(self):
        """Remove the keyboard focus from all the segments that have it"""
        for box in self._boxes_with_keyboard_focus:
            box.set_keyboard_focus(False)
        self._boxes_with_keyboard_focus = []

    def get_selection_box(self):
        """Return the bounding box of selected items

        Returns
        --------
        tuple : (top_left, bottom_right) where each tuple is formed of (x,y) or
            None if there is no selection
        """
        tl = None
        br = None
        for item in self.selectedItems():
            box = item.boundingRect()
            if tl is None:
                tl = (box.left(), box.top())
                br = (box.right(), box.bottom())
            else:
                tl = (min(tl[0], box.left()), min(tl[1], box.top()))
                br = (max(br[0], box.right()), max(br[1], box.bottom()))
        if tl is None:
            return None
        return tl, br

    def get_segment_pixmap(self, segment, width, height=None, fit=True,
                           background='#EEE', border=True, padding=16):
        """Extract a segment's pixmap for use in GUI elements.

        The extracted pixmap is scaled to fit within width*height. If fit
        is True the returned image will be exactly width*height, with the
        background filled with the given color.

        Parameters
        ----------
        segment : Segment
        width, height : float or int
            Dimensions to scale the pixmap to. If height is None, it is set
            to width (ie. a square)
        fit : bool
            If True, the returned image will be exactly width*height
        background : str or QColor or QBrush
            If the image was padded (either to make it fit, or for padding)
            the background is filled with this color
        border : bool
            If True, a border is added around the image. This is drawn inside
            the image, and does not affect the returned width/height
        padding : int
            Padding to add around the segment within the returned image. This
            does not affect the returned width/height

        Returns
        -------
        QtGui.QPixmap
        """
        # Get the rectangle and calculate the scale factor
        rect = segment.get_q_rect_f()
        if height is None:
            height = width
        w_scale = (float(width) - float(padding))/rect.width()
        h_scale = (float(height) - float(padding))/rect.height()
        scale = min(w_scale, h_scale)

        # Extract the pixmap
        pixmap = self._pixmap.copy(
            int(rect.left()), int(rect.top()),
            int(rect.width()), int(rect.height())
        )
        pixmap = pixmap.scaled(
            pixmap.width() * scale,
            pixmap.height() * scale,
            transformMode=QtCore.Qt.SmoothTransformation
        )
        if not fit and padding == 0:
            return pixmap
        if type(background) is str:
            background = QtGui.QColor(background)
        background_pixmap = QtGui.QPixmap(width, height)
        painter = QtGui.QPainter(background_pixmap)
        painter.fillRect(QtCore.QRectF(0, 0, width, height), background)
        painter.drawPixmap(
            (width - pixmap.width()) / 2,
            (height - pixmap.height()) / 2,
            pixmap
        )
        if border:
            painter.setPen(QtCore.Qt.DashLine)
            painter.drawRect(QtCore.QRectF(0, 0, width - 1, height - 1))
        painter.end()
        return background_pixmap

    def _after_segment_add(self, segment):
        """Callback invoked when a new segment is added

        Parameters
        ----------
        segment : Segment
        """
        box = BoxResizable(self, segment)
        segment.associate_object(box)

    def _before_segment_remove(self, segment):
        """Callback invoked when a segment is removed

        Parameters
        ----------
        segment : Segment
        """
        box = segment.get_associated_object(BoxResizable)
        self.removeItem(box)