from PySide import QtGui, QtCore


class MouseEvents(object):
    def __init__(self, parent_class):
        self.parent_class = parent_class

        self._mouse_state = {
            'button': None,
            'pressed_at': None
        }

    def _mouse_left(self, x, y):
        pass

    def _mouse_right(self, x, y):
        pass

    def _mouse_middle(self, x, y):
        pass

    def _mouse_left_release(self, x, y):
        pass

    def _mouse_right_release(self, x, y):
        pass

    def _mouse_middle_release(self, x, y):
        pass

    def _mouse_move(self, x, y):
        pass

    def _mouse_enter(self, x, y):
        pass

    def _mouse_leave(self, x, y):
        pass

    def _mouse_wheel(self, delta, ctrl=False, shift=False):
        pass

    def mousePressEvent(self, event):
        self.parent_class.mousePressEvent(self, event)

        x = event.pos().x()
        y = event.pos().y()

        state = self._mouse_state
        state['pressed_at'] = (x, y)

        if event.button() == QtCore.Qt.MidButton:
            self._mouse_middle(x, y)
            state['button'] = 'middle'

        elif event.button() == QtCore.Qt.LeftButton:
            self._mouse_left(x, y)
            state['button'] = 'left'

        elif event.button() == QtCore.Qt.RightButton:
            self._mouse_right(x, y)
            state['button'] = 'right'

    def mouseMoveEvent(self, event):
        self.parent_class.mouseMoveEvent(self, event)

        if self._mouse_state['button'] is None:
            event.ignore()
            return

        x = event.pos().x()
        y = event.pos().y()

        self._mouse_move(x, y)

        event.accept()

    def mouseReleaseEvent(self, event):
        self.parent_class.mouseReleaseEvent(self, event)

        x = event.pos().x()
        y = event.pos().y()

        if event.button() == QtCore.Qt.MidButton:
            self._mouse_middle_release(x, y)
        elif event.button() == QtCore.Qt.RightButton:
            self._mouse_right_release(x, y)
        elif event.button() == QtCore.Qt.LeftButton:
            self._mouse_left_release(x, y)

        self._mouse_state['button'] = None
        self._mouse_state['pressed_at'] = None

    def hoverEnterEvent(self, event):
        self.parent_class.hoverEnterEvent(self, event)

        x = event.pos().x()
        y = event.pos().y()

        self._mouse_enter(x, y)

    def hoverLeaveEvent(self, event):
        self.parent_class.hoverLeaveEvent(self, event)

        x = event.pos().x()
        y = event.pos().y()

        self._mouse_leave(x, y)

    def wheelEvent(self, event):
        self.parent_class.wheelEvent(self, event)

        delta = event.delta()

        ctrl = event.modifiers() & QtCore.Qt.ControlModifier
        shift = event.modifiers() & QtCore.Qt.ShiftModifier
        self._mouse_wheel(delta, ctrl=ctrl, shift=shift)
