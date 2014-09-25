import weakref
import inselect.settings
from inselect.lib.segment_object import Segment
from PySide import QtCore, QtGui


class SegmentNotInScene(Exception):
    """Exception raised when attempting an operation on a segment which is not
    part of the scene"""
    pass


class NoAssociatedObject(Exception):
    """Exception raised when attempting to obtain a non-existent
    associated object
    """
    pass


class SegmentScene(object):
    """The SegmentScene keeps track of all segments in a scene, giving context
    to the normalized segments and providing a way for UI elements to get
    notifications in changes in the scene.

    The list of segment is ordered in an intuitive prev/next fashion, and
    updated whenever a segment is modified.

    The segment scene allows other components to add watchers, to track the
    following events: 'after-segment-add', 'before-segment-remove'.
    Because segments can be modified directly, events to track update of
    individual segments are on the Segment objects themselves.

    The segment scene can also keep track of objects associated with a
    particular segment using `associate_object` and `get_associated_object`.
    This is useful for the UI to keep track of UI components associated with
    a segment.

    Notes
    -----
    - The individual segments are normalized - only the segment scene has
      knowledge of the context in which the segments are drawn. So any
      operation based on screen co-ordinates need to go through
      the SegmentScene.

    - Associating an object does not create an additional reference to the
      object. It must be kept track of elsewhere.

    Parameters
    ----------
    width, height : float or int
        Width and height of the scene
    """
    def __init__(self, width, height):
        self._width = float(width)
        self._height = float(height)
        self._pixmap = None
        self._segments = []
        self._watchers = {
            'after-segment-add': [],
            'before-segment-remove': []
        }

    def add(self, corner_a, corner_b, fields=None):
        """Add a segment from non-normalized (scene) coordinates

        corner_a and corner_b should both represent one corner of the box,
        such that the two corners are diagonally opposite. These will always
        be re-arranged and stored as (top left, bottom right).

        Parameters
        ----------
        corner_a, corner_b : tuple of float or int
            Each corner is (x, y)
        fields : dict, optional

        Returns
        -------
        Segment
            The created segment
        """
        self.add_normalized(
            (float(corner_a[0])/self._width, float(corner_a[1])/self._height),
            (float(corner_b[0])/self._width, float(corner_b[1])/self._height),
            fields
        )

    def add_normalized(self, corner_a, corner_b, fields=None):
        """Add a segment from normalized coordinates

        corner_a and corner_b should both represent one corner of the box,
        such that the two corners are diagonally opposite. These will always
        be re-arranged and stored as (top left, bottom right).

        Parameters
        ----------
        corner_a, corner_b : tuple of float or int
            Each corner is (x, y)
        fields : dict, optional

        Returns
        -------
        Segment
            The created segment
        """
        new_segment = Segment(
            (float(corner_a[0]), float(corner_a[1])),
            (float(corner_b[0]), float(corner_b[1])),
            fields
        )
        self._insert(new_segment)
        for callback in self._watchers['after-segment-add']:
            callback(new_segment)
        return new_segment

    def remove(self, segment):
        """Remove a segment from the scene

        Parameters
        ----------
        segment : segment to remove
        """
        # Ensure we own it.
        self.get_segment_index(segment)
        for callback in self._watchers['before-segment-remove']:
            callback(segment)
        # We don't need to check for ValueError here - if someone attempted
        # to remove the segment again it would have caused a loop!
        index = self.get_segment_index(segment)
        del self._segments[index]

    def segments(self):
        """Return a list of the scene's segments

        Returns
        -------
        list of Segment
        """
        segments = []
        for s in self._segments:
            segments.append(s['segment'])
        return segments

    def watch(self, watch_type, callback):
        """Add a callback to be invoked when the segment scene is updated

        Parameters
        ----------
        watch_type : str
            Action to watch. One of 'after-segment-add'
            and 'before-segment-remove'
        callback : function
            Invoked when the segment is updated with the segment as parameter
        """
        self._watchers[watch_type].append(callback)

    def _insert(self, new_segment, objects=None):
        """Insert a new segment in the scene

        Parameters
        ----------
        new_segment : Segment
        objects : dict of name to weakref, optional
            List of objects associated with the segment, stored as weak
            references
        """
        # Basic insertion algorithm: divide the scene in 20 bands, and order
        # the segments per band (based on top left corner). Within each band,
        # order the segments by x coordinate.
        band_size = 1.0/20.0
        new_segment_band = int(new_segment.top()/band_size)
        insert_at = len(self._segments)
        for i in range(len(self._segments)):
            segment = self._segments[i]['segment']
            segment_band = segment.top()/band_size
            if new_segment_band > segment_band:
                continue
            if (new_segment_band < segment_band or
                    new_segment.left() < segment.left()):
                insert_at = i
                break
        if objects is None:
            objects = {}
        self._segments.insert(insert_at, {
            'segment': new_segment,
            'objects': objects
        })

    def set_segment_corners(self, segment, top_left, bottom_right):
        """set the given segment's corners from non-normalized (scene)
        coordinates.

        Parameters
        ----------
        segment : Segment
            The segment to update in the context of this scene
        top_left, bottom_right : tuple of float or int
            New co-ordinates

        Raises
        ------
        SegmentNotInScene
        """
        # Ensure we own it.
        self.get_segment_index(segment)
        top_left = (
            float(top_left[0]) / self._width,
            float(top_left[1]) / self._height
        )
        bottom_right = (
            float(bottom_right[0]) / self._width,
            float(bottom_right[1]) / self._height
        )
        segment.set_corners(top_left, bottom_right)
        # Now update the scene
        try:
            index = self.get_segment_index(segment)
        except SegmentNotInScene:
            # One of the watchers decided to delete the segment. That's fine.
            return
        objects = self._segments[index]['objects']
        del self._segments[index]
        self._insert(segment, objects)

    def move_segment_corners(self, segment, top_left_delta,
                               bottom_right_delta=None):
        """Update the given segment's corners from
        non-normalized (scene) deltas.

        This will either update both the top left and bottom right corners
        independently (if both top_left_delta and bottom_right_delta) are
        defined, or will move both corners equally (if only top_left_delta
        is defined)

        Parameters
        ----------
        segment : Segment
            The segment to update in the context of this scene
        top_left_delta : tuple of float or int
        bottom_right_delta : tuple of float or int, optional

        Raises
        ------
        SegmentNotInScene
        """
        # Ensure we own it.
        self.get_segment_index(segment)
        top_left_delta = (
            float(top_left_delta[0]) / self._width,
            float(top_left_delta[1]) / self._height
        )
        if bottom_right_delta:
            bottom_right_delta = (
                float(bottom_right_delta[0]) / self._width,
                float(bottom_right_delta[1]) / self._height
            )
        segment.move_corners(top_left_delta, bottom_right_delta)
        # Now update the scene
        try:
            index = self.get_segment_index(segment)
        except SegmentNotInScene:
            # One of the watchers decided to delete the segment. That's fine.
            return
        objects = self._segments[index]['objects']
        del self._segments[index]
        self._insert(segment, objects)

    def set_size(self, width, height):
        """Sets the size of the scene and re-normalize segments

        Parameters
        ----------
        width, height : float or int
            New width and height fo the scene.
        """
        w_factor = self._width / float(width)
        h_factor = self._height / float(height)
        for s in self._segments:
            s['segment'].renormalize(w_factor, h_factor)
        self._width = float(width)
        self._height = float(height)

    def set_pixmap(self, pixmap):
        """Sets the pixmap of the scene.

        This will re-set the width/height of the scene, and re-normalize
        segments.

        Parameters
        ----------
        pixmap : QPixmap
        """
        self._pixmap = pixmap
        self.set_size(pixmap.width(), pixmap.height())

    def empty(self):
        """Remove all the segments"""
        for s in self._segments:
            s['segment'].prepare_for_remove()
        self._segments = []

    def get_segment_index(self, segment):
        """Get the index of the given segment

        Parameters
        ----------
        segment : Segment

        Returns
        -------
        int

        Raises
        ------
        ValueError
            If the segment is not in the scene
        """
        for index in range(len(self._segments)):
            if self._segments[index]['segment'] is segment:
                return index
        raise ValueError()

    def get_next_segment(self, segment):
        """Return the segment that follows the given one

        Parameters
        ----------
        segment : Segment or None
            If None return the first segment

        Returns
        -------
        Segment or None
            Returns None if there are no segments

        Raises
        ------
        ValueError
            If the segment is not in the scene
        """
        if len(self._segments) == 0:
            return None
        if segment is None:
            segment_index = 0
        else:
            pos = self.get_segment_index(segment)
            segment_index = (pos + 1) % len(self._segments)
        return self._segments[segment_index]['segment']

    def get_previous_segment(self, segment):
        """Return the segment that precedes the given one

        Parameters
        ----------
        segment : Segment or None
            If None return the first segment

        Returns
        -------
        Segment or None
            Returns None if there are no segments

        Raises
        ------
        ValueError
            If the segment is not in the scene
        """
        if len(self._segments) == 0:
            return None
        if segment is None:
            segment_index = 0
        else:
            pos = self.get_segment_index(segment)
            segment_index = (pos - 1) % len(self._segments)
        return self._segments[segment_index]['segment']

    def get_q_rect_f(self, segment):
        """Return a de-normalized QRectF object representing a segment

        A new QRectF object is build every time.

        Parameters
        ----------
        segment : Segment

        Returns
        -------
        QtCore.QRectF
        """
        return QtCore.QRectF(
            segment.left() * self._width,
            segment.top() * self._height,
            segment.width() * self._width,
            segment.height() * self._height
        )

    def get_segment_icon(self, segment):
        """Return a segment's icon in the scene

        The scene must have a pixmap for this to work.

        Parameters
        ----------
        segment : Segment

        Returns
        -------
        QtGui.QIcon
        """
        icon_size = inselect.settings.get('icon_size')
        icon_padding = 16
        icon_background = '#EEE'
        self.get_segment_index(segment)
        # Get a scale the selected segment to fit in the icon size
        pixmap = self._pixmap.copy(
            int(segment.left() * self._width),
            int(segment.top() * self._height),
            int(segment.width() * self._width),
            int(segment.height() * self._width)
        )
        if pixmap.width() > pixmap.height():
            scale = float(icon_size - icon_padding)/float(pixmap.width())
        else:
            scale = float(icon_size - icon_padding)/float(pixmap.height())
        pixmap = pixmap.scaled(
            pixmap.width() * scale,
            pixmap.height() * scale,
            transformMode=QtCore.Qt.SmoothTransformation
        )
        # Create a background pixmap
        background = QtGui.QPixmap(icon_size, icon_size)
        painter = QtGui.QPainter(background)
        painter.fillRect(QtCore.QRectF(0, 0, icon_size-1, icon_size-1),
                         QtGui.QColor(icon_background))
        painter.setPen(QtCore.Qt.DashLine)
        painter.drawRect(QtCore.QRectF(0, 0, icon_size-1, icon_size-1))
        painter.drawPixmap(
            (icon_size - pixmap.width()) / 2,
            (icon_size - pixmap.height()) / 2,
            pixmap
        )
        painter.end()
        # Create the icon
        icon = QtGui.QIcon()
        icon.addPixmap(background)
        return icon

    def associate_object(self, name, obj, segment):
        """Associate an object with a particular segment in this scene

        Parameters
        ----------
        name : str
            Name to store the object under
        obj : object
            Object to associate with the segment
        segment : Segment
            Segment to associate the object with

        Raises
        ------
        ValueError
            If the segment is not in this scene
        """
        index = self.get_segment_index(segment)
        self._segments[index]['objects'][name] = weakref.ref(obj)

    def get_associated_object(self, name, segment):
        """Return an object associated with a segment in this scene

        Notes
        -----
        A weak reference to an object that gets GCed becomes None. Given that
        there is no practical use for storing None here, we always assume
        a value of None means there is no object anymore.

        Parameters
        ----------
        name : str
            Name the object was associated as
        segment : Segment
            Segment the object was associated with

        Returns
        -------
        object
            The associated object

        Raises
        ------
        ValueError
            If the segment is not in the scene
        NoAssociatedObject
            If there is no such associated object for the segment
        """
        index = self.get_segment_index(segment)
        objs = self._segments[index]['objects']
        if name in objs:
            deref = (objs[name])()
            if deref is not None:
                return deref
        raise NoAssociatedObject()

    def get_associated_segment(self, obj):
        """Return a segment associated with an object in this scene

        Parameters
        ----------
        object : associated object

        Returns
        -------
        Segment
            The associated segment

        Raises
        ------
        NoAssociatedOjbect
            If the object is not found in the scene
        """
        for s in self._segments:
            for name in s['objects']:
                deref = (s['objects'][name])()
                if deref is obj:
                    return s['segment']
        raise NoAssociatedObject()
