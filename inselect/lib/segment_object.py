import weakref
import inspect
from PySide import QtCore
from inselect.gui  import utils


class NoAssociatedObject(Exception):
    """Exception raised when attempting to obtain a non-existent
    associated object
    """
    pass


class Segment(object):
    """This class represents an individual segment in a scene and a set of
    field/values.

    It is possible to get callbacks invoked when a segment is updated, by
    adding a watcher using `watch`. There are two types of events that can
    be watched: `after-fields-update` and `after-corners-update`

    Parameters
    ----------
    corner_a, corner_b : tuple of float
      corner_a and corner_b should both represent one corner of the box (as an
      (x, y) tuple), such that the two corners are diagonally opposite. These
      will always be re-arranged and stored as (top left, bottom right).
    scene_size : tuple of float
        (width, height) of the scene this segments belongs to. If None,
        it is assume the segment is already normalized (ie. the size
        is (1, 1))
    fields : dictionary, None
        Fields values for this segment
    """
    def __init__(self, corner_a, corner_b, scene_size=None, fields=None):
        self._rect = [[0, 0], [0, 0]]
        self._width = 0
        self._height = 0
        self._watchers = {
            'after-fields-update': [],
            'after-corners-update': []
        }
        self._objects = {}
        if fields is None:
            self._fields = {}
        else:
            self._fields = dict(fields)
        if scene_size is None:
            self._scene_size = (1.0, 1.0)
        else:
            self._scene_size = (float(scene_size[0]), float(scene_size[1]))
        self._seeds = []
        self.set_corners(corner_a, corner_b)

    def set_corners(self, corner_a, corner_b):
        """Set the rectangle corners, for scene co-ordinates

        corner_a and corner_b should both represent one corner of the box,
        such that the two corners are diagonally opposite. These will always
        be re-arranged and stored as (top left, bottom right).

        Parameters
        ----------
        corner_a, corner_b: tuple of float
            Each corner is (x, y)
        """
        ((x1, y1), (x2, y2)) = utils.get_corners(corner_a[0], corner_a[1],
                                                 corner_b[0], corner_b[1])
        self._rect = [[x1, y1], [x2, y2]]
        self._width = x2 - x1
        self._height = y2 - y1
        for callback in self._watchers['after-corners-update']:
            callback(self)

    def move_corners(self, top_left_delta, bottom_right_delta=None):
        """Move the given segment's corners, from scene co-ordinates

        This will either update both the top left and bottom right corners
        independently (if both top_left_delta and bottom_right_delta) are
        defined, or will move both corners equally (if only top_left_delta
        is defined)

        Parameters
        ----------
        top_left_delta : tuple of float
        bottom_right_delta : tuple of float, optional
        """
        top_left = (
            self._rect[0][0] + top_left_delta[0],
            self._rect[0][1] + top_left_delta[1]
        )
        if bottom_right_delta:
            bottom_right = (
                self._rect[1][0] + bottom_right_delta[0],
                self._rect[1][1] + bottom_right_delta[1]
            )
        else:
            bottom_right = (
                self._rect[1][0] + top_left_delta[0],
                self._rect[1][1] + top_left_delta[1]
            )
        self.set_corners(top_left, bottom_right)

    def set_scene_size(self, width, height):
        """Set the scene size and scale segment accordingly

        Notes
        -----
        This does not trigger a 'after-corners-update' event

        Parameters
        ----------
        width, height : float or int
            New size of the scene
        """
        w_factor = self._scene_size[0] / float(width)
        h_factor = self._scene_size[1] / float(height)
        self._scene_size = (float(width), float(height))
        self._rect = [
            [
                self._rect[0][0] * w_factor,
                self._rect[0][1] * h_factor
            ],
            [
                self._rect[1][0] * w_factor,
                self._rect[1][1] * h_factor
            ]
        ]
        self._width = self._rect[1][0] - self._rect[0][0]
        self._height = self._rect[1][1] - self._rect[0][1]

    def watch(self, watch_type, callback):
        """Add a callback to be invoked when the segment is updated

        Parameters
        ----------
        watch_type : str
            Action to watch. One of 'after-fields-update',
            'after-corners-update'
        callback : function
            Invoked when the segment is updated with the segment as parameter
        """
        self._watchers[watch_type].append(callback)

    def rect(self, normalized=False):
        """Return the segment rectangle as ((x1, y1), (x2, y2)) such that
        (x1, y1) is the top left corner, and (x2, y2) the bottom right corner.

        Parameters
        ----------
        normalized : bool
            If True, the normalized segment is returned

        Returns
        -------
        tuple of tuple of floats
            ((x1, y1), (x2, y2))
        """
        if normalized:
            return (
                (
                    self._rect[0][0] / self._scene_size[0],
                    self._rect[0][1] / self._scene_size[1]
                ),
                (
                    self._rect[1][0] / self._scene_size[0],
                    self._rect[1][1] / self._scene_size[1]
                )
            )
        else:
            return (
                (self._rect[0][0], self._rect[0][1]),
                (self._rect[1][0], self._rect[1][1])
            )

    def get_q_rect_f(self, normalized=False):
        """Return the segment as QtCore.QRectF object

        Note the object is re-build at each invocation.

        Parameters
        ----------
        normalized : bool
            If True, return the normalized co-ordinates

        Returns
        -------
        QtCore.QRectF
        """
        if normalized:
            rect = self.rect(normalized=True)
            return QtCore.QRectF(
                rect[0][0], rect[0][1],
                rect[1][0] - rect[0][0], rect[1][1] - rect[0][1]
            )
        else:
            return QtCore.QRectF(
                self._rect[0][0], self._rect[0][1], self._width, self._height
            )

    def left(self, normalized=False):
        """Return the coordinate of the left side of the box

        Parameters
        ----------
        normalized : bool
            If True, return the normalized co-ordinate

        Returns
        -------
        float
        """
        if normalized:
            return self._rect[0][0] / self._scene_size[0]
        else:
            return self._rect[0][0]

    def top(self, normalized=False):
        """Return the coordinate of the top side of the box

        Parameters
        ----------
        normalized : bool
            If True, return the normalized co-ordinate

        Returns
        -------
        float
        """
        if normalized:
            return self._rect[0][1] / self._scene_size[1]
        else:
            return self._rect[0][1]

    def right(self, normalized=False):
        """Return the coordinate of the right side of the box

        Parameters
        ----------
        normalized : bool
            If True, return the normalized co-ordinate

        Returns
        -------
        float
        """
        if normalized:
            return self._rect[1][0] / self._scene_size[0]
        else:
            return self._rect[1][0]

    def bottom(self, normalized=False):
        """Return the coordinate of the bottom side of the box

        Parameters
        ----------
        normalized : bool
            If True, return the normalized co-ordinate

        Returns
        -------
        float
        """
        if normalized:
            return self._rect[1][1] / self._scene_size[1]
        else:
            return self._rect[1][1]

    def width(self, normalized=False):
        """Return the width of the box

        Parameters
        ----------
        normalized : bool
            If True, return the normalized width

        Returns
        -------
        float
        """
        if normalized:
            return self._width / self._scene_size[0]
        else:
            return self._width

    def height(self, normalized=False):
        """Return the height of the box

        Parameters
        ----------
        normalized : bool
            If True, return the normalized height

        Returns
        -------
        float
        """
        if normalized:
            return self._height / self._scene_size[1]
        else:
            return self._height

    def fields(self):
        """Return (a copy of) the segment's fields

        Returns
        -------
        dict
        """
        return dict(self._fields)

    def set_field(self, name, value):
        """Set a field value on this segment

        Parameters
        ----------
        name : str
        value : object
        """
        self._fields[name] = value
        for callback in self._watchers['after-fields-update']:
            callback(self)

    def empty_seeds(self):
        """Remove all seeds added to this segment"""
        self._seeds = []

    def add_seed(self, seed):
        """Add a new seed to this segment

        Parameters
        ----------
        seed : tuple of floats
        """
        self._seeds.append(seed)

    def seeds(self):
        """Return this segment's seeds

        Returns
        -------
        list
        """
        return list(self._seeds)

    def associate_object(self, obj, name=None):
        """Associate an object with that segment.

        This is useful for UI components to keep track of each other.

        Notes
        -----
        - By default the association is done using the given object's class
          name. This approach covers the main use case we have for this
          (associate a UI object with a segment)
        - The association is stored using a weak reference, so will not prevent
          an object from being GCed.

        Parameters
        ----------
        obj : object
            Object to associate with the segment
        name : str
            The identifier to associate the object under. If None,
            the obj.__class__.__name__ will be used.
        """
        if name is None:
            name = obj.__class__.__name__
        self._objects[name] = weakref.ref(obj)

    def get_associated_object(self, name):
        """Return an object associated with this segment

        Notes
        -----
        A weak reference to an object that gets GCed becomes None. Given that
        there is no practical use for storing None here, we always assume
        a value of None means there is no object anymore.

        Parameters
        ----------
        name : str or classobj
            Name the object was associated as. If a class object, then the
            associated name is name.__name__

        Returns
        -------
        object
            The associated object

        Raises
        ------
        NoAssociatedObject
            If there is no such associated object for the segment
        """
        if inspect.isclass(name):
            name = name.__name__
        if name in self._objects:
            deref = (self._objects[name])()
            if deref is not None:
                return deref
        raise NoAssociatedObject()

    def is_associated_to(self, obj):
        """Checks if this segment is associated to the given object

        Parameters
        ----------
        obj : object
            Object to check against

        Returns
        -------
        bool
        """
        for name in self._objects:
            deref = (self._objects[name])()
            if deref is obj:
                return True
        return False
