from inselect.lib.segment_object import Segment, NoAssociatedObject


class SegmentNotInScene(Exception):
    """Exception raised when attempting an operation on a segment which is not
    part of the scene"""
    pass


class SegmentScene(object):
    """The SegmentScene keeps track of all segments in a scene.

    The list of segment is ordered in an intuitive prev/next fashion, and
    updated whenever a segment is modified.

    The segment scene allows other components to add watchers, to track the
    following events: 'after-segment-add', 'before-segment-remove'.
    Because segments can be modified directly, events to track update of
    individual segments are on the Segment objects themselves.

    Parameters
    ----------
    width, height : float or int
        Width and height of the scene. Both default to '1', creating a
        normalized scene.
    """
    def __init__(self, width=1, height=1):
        self._width = float(width)
        self._height = float(height)
        self._segments = []
        self._watchers = {
            'after-segment-add': [],
            'before-segment-remove': []
        }

    def add(self, corner_a, corner_b, fields=None):
        """Add a segment from scene coordinates

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
            (self._width, self._height),
            fields
        )
        self._insert(new_segment)
        # Ensure we are the first watcher, so the segment scene is always
        # ordered correctly.
        new_segment.watch('after-corners-update', self._segment_moved)
        for callback in self._watchers['after-segment-add']:
            callback(new_segment)
        return new_segment

    def add_normalized(self, corner_a, corner_b, fields=None):
        """Add a segment from normalized coordinates

        corner_a and corner_b should both represent one corner of the box,
        such that the two corners are diagonally opposite. These will always
        be re-arranged and stored as (top left, bottom right).

        Parameters
        ----------
        corner_a, corner_b : tuple of float
            Each corner is (x, y)
        fields : dict, optional

        Returns
        -------
        Segment
            The created segment
        """
        return self.add(
            (corner_a[0] * self._width, corner_a[1] * self._height),
            (corner_b[0] * self._width, corner_b[1] * self._height),
            fields
        )

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
        return list(self._segments)

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

    def _insert(self, new_segment):
        """Insert a new segment in the scene

        Parameters
        ----------
        new_segment : Segment
        """
        # Basic insertion algorithm: divide the scene in 20 bands, and order
        # the segments per band (based on top left corner). Within each band,
        # order the segments by x coordinate.
        band_size = 1.0/20.0
        new_segment_band = int(new_segment.top()/band_size)
        insert_at = len(self._segments)
        for i in range(len(self._segments)):
            segment = self._segments[i]
            segment_band = segment.top()/band_size
            if new_segment_band > segment_band:
                continue
            if (new_segment_band < segment_band or
                    new_segment.left() < segment.left()):
                insert_at = i
                break
        self._segments.insert(insert_at, new_segment)

    def _segment_moved(self, segment):
        """Call to notify the segment scene a segment has moved

        This allows us to re-order the list

        Parameters
        ----------
        segment : Segment
        """
        index = self.get_segment_index(segment)
        del self._segments[index]
        self._insert(segment)

    def set_size(self, width, height):
        """Sets the size of the scene and scale segments accordingly

        Parameters
        ----------
        width, height : float or int
            New width and height fo the scene.
        """
        self._width = float(width)
        self._height = float(height)
        for segment in self._segments:
            segment.set_scene_size(self._width, self._height)

    def empty(self):
        """Remove all the segments"""
        for segment in self._segments:
            segment.prepare_for_remove()
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
        return self._segments.index(segment)

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
        return self._segments[segment_index]

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
        return self._segments[segment_index]

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
        NoAssociatedObject
            If the object is not found in the scene
        """
        for segment in self._segments:
            if segment.is_associated_to(obj):
                return segment
        raise NoAssociatedObject()
