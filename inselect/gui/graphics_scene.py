from PySide import QtGui
from inselect.gui.box_resizable import BoxResizable


class GraphicsScene(QtGui.QGraphicsScene):
    """The GraphicsScene holds all the boxes displayed to the user.

    The GraphicsScene listens for segments being added/removed to the
    segment scene, and adds/removes BoxResizable items to the scene
    correspondingly.
    """
    def __init__(self, segment_scene):
        QtGui.QGraphicsScene.__init__(self)
        self._segment_scene = segment_scene
        self._segment_scene.watch('after-segment-add', self._after_segment_add)
        self._segment_scene.watch('before-segment-remove',
                                  self._before_segment_remove)

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

    def _after_segment_add(self, segment):
        """Callback invoked when a new segment is added

        Parameters
        ----------
        segment : Segment
        """
        box = BoxResizable(self, self._segment_scene, segment)
        self._segment_scene.associate_object('boxResizable', box, segment)

    def _before_segment_remove(self, segment):
        """Callback invoked when a segment is removed

        Parameters
        ----------
        segment : Segment
        """
        box = self._segment_scene.get_associated_object('boxResizable', segment)
        self.removeItem(box)