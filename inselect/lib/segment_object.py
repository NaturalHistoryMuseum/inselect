from inselect.lib import utils


class Segment(object):
    """This class represents an individual segment, represented by
    normalized coordinates and a set of field/values.

    The Segment does not store information about the context in which it was
    created. To use scene co-ordinates, the segment must be created/updated
    through the SegmentScene.

    It is possible to get callbacks invoked when a segment is updated, by
    adding a watcher using `watch`. There are two types of events that can
    be watched: `after-fields-update` and `after-corners-update`

    Parameters
    ----------
    corner_a, corner_b : tuple of float
      corner_a and corner_b should both represent one corner of the box (as an
      (x, y) tuple), such that the two corners are diagonally opposite. These
      will always be re-arranged and stored as (top left, bottom right).
    fields : dictionary, None
        Fields values for this segment
    """
    def __init__(self, corner_a, corner_b, fields=None):
        self._rect = [[0, 0], [0, 0]]
        self._width = 0
        self._height = 0
        self._watchers = {
            'after-fields-update': [],
            'after-corners-update': []
        }
        if fields is None:
            self._fields = {}
        else:
            self._fields = dict(fields)
        self._seeds = []
        self.set_corners(corner_a, corner_b)

    def set_corners(self, corner_a, corner_b):
        """Set the rectangle corners

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
        """Move the given segment's corners.

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

    def rect(self):
        """Return the normalized rectangle as ((x1, y1), (x2, y2)) such that
        (x1, y1) is the top left corner, and (x2, y2) the bottom right corner.

        Returns
        -------
        tuple
        """
        return (
            (self._rect[0][0], self._rect[0][1]),
            (self._rect[1][0], self._rect[1][1])
        )

    def renormalize(self, x_factor, y_factor):
        """Renormalize the segment by applying the given factor

        Parameters
        ----------
        x_factor, y_factor : float
        """
        self._rect = [
            [self._rect[0][0] * x_factor, self._rect[0][1] * y_factor],
            [self._rect[1][0] * x_factor, self._rect[1][1] * y_factor]
        ]
        self._width = self._rect[1][0] - self._rect[0][0]
        self._height = self._rect[1][1] - self._rect[0][1]

    def left(self):
        """Return the coordinate of the left side of the box

        Returns
        -------
        float
        """
        return self._rect[0][0]

    def top(self):
        """Return the coordinate of the top side of the box

        Returns
        -------
        float
        """
        return self._rect[0][1]

    def right(self):
        """Return the coordinate of the right side of the box

        Returns
        -------
        float
        """
        return self._rect[1][0]

    def bottom(self):
        """Return the coordinate of the bottom side of the box

        Returns
        -------
        float
        """
        return self._rect[1][1]

    def width(self):
        """Return the width of the box

        Returns
        -------
        float
        """
        return self._width

    def height(self):
        """Return the height of the box

        Returns
        -------
        float
        """
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