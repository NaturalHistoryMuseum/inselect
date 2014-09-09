from PySide import QtGui, QtCore


class MouseEvents(object):
    """Mixin used to map mouse events to methods.

    The mixin implements Qt mouse events methods, so classes should not implement their own
    """
    def __init__(self, parent_class):
        self.parent_class = parent_class

        self._last_position = (0, 0)
        self._mouse_state = {
            'button': None,
            'pressed_at': None,
            'delta': (0, 0)
        }

        self._handlers = {}

    def add_mouse_handler(self, event, callback, *args):
        """Add a new mouse handler

        Parameters
        ----------
        event : str, tuple
            see `_get_event`
        callback : function
            Function to call on event. The function should return True to allow 
            the event to propagate, False otherwise.
        *args
            Additional arguments will be passed to the callback methods, *after* the event
            specific arguments.
        """
        (event, button, modifier) = self._get_event(event)
        if event not in self._handlers:
            self._handlers[event] = {}
        if button not in self._handlers[event]:
            self._handlers[event][button] = {}
        if modifier not in self._handlers[event][button]:
            self._handlers[event][button][modifier] = []
        self._handlers[event][button][modifier].append((callback, args))

    def _get_event(self, event):
        """Return a (event, button, modifier) tuple for the given event

        Parameters
        ----------
        event : str, tuple
            May be an event name, a tuple defining (event, button) or a tuple
            defining (event, button, modifier) where:
                - event is one of 'press', 'release', 'wheel', 'move', 'enter', 'leave';
                - button is one of 'right', 'left', 'middle', 'none';
                - modifier is a Qt modifier constant
                
        Returns
        -------
        tuple
            An (event, button, modifier) tuple
        """
        event_str = event
        button = 'none'
        modifier = int(QtCore.Qt.NoModifier)
        if isinstance(event, (list, tuple)):
            event_str = event[0]
            if len(event) > 1 and event[1] is not None:
                button = event[1]
            if len(event) > 2:
                modifier = int(event[2])

        return (event_str, button, modifier)

    def _handle_event(self, event, *args):
        """Handle an event by calling appropriate handlers

        Parameters
        ----------
        event : tuple
            Tuple as (event, button, modifier). See `_get_event`
        *args
            Additional arguments, that are passed to the callback function *before*
            the additional arguments defined when creating the handler.

        Returns
        -------
        bool
            True to allow the event to propagate, False otherwise.
        """
        (event_str, button, modifier) = event
        button = button or 'none'
        try:
            handlers = self._handlers[event_str][button][modifier]
        except KeyError:
            return True
        propagate = True
        for (callback, handler_args) in handlers:
            propagate = propagate & callback(*(args + handler_args))
        return propagate

    def mousePressEvent(self, event):
        """Handle mouse press events

        Parameters
        ----------
        event : QtEvent
        """
        x = event.pos().x()
        y = event.pos().y()

        state = self._mouse_state
        state['pressed_at'] = (x,y)
        if event.button() == QtCore.Qt.MidButton:
            state['button'] = 'middle'
        elif event.button() == QtCore.Qt.LeftButton:
            state['button'] = 'left'
        elif event.button() == QtCore.Qt.RightButton:
            state['button'] = 'right'

        propagate = self._handle_event(('press', state['button'], int(event.modifiers())), x, y)
        if propagate:
            self.parent_class.mousePressEvent(self, event)
        else:
            event.accept()

    def mouseMoveEvent(self, event):
        """Handle mouse move events

        Parameters
        ----------
        event : QtEvent
        """
        x = event.pos().x()
        y = event.pos().y()
        button = self._mouse_state['button']
        self._mouse_state['delta'] = (self._last_position[0] - x, self._last_position[1] - y)
        propagate = self._handle_event(('move', button, int(event.modifiers())), x, y)
        if propagate:
            self.parent_class.mouseMoveEvent(self, event)
        else:
            event.accept()
        self._last_position = (x, y)

    def mouseReleaseEvent(self, event):
        """Handle mouse release events

        Parameters
        ----------
        event : QtEvent
        """
        x = event.pos().x()
        y = event.pos().y()
        button = self._mouse_state['button']
        propagate = self._handle_event(('release', button, int(event.modifiers())), x, y)
        if propagate:
            self.parent_class.mouseReleaseEvent(self, event)
        else:
            event.accept()

        self._mouse_state['button'] = None
        self._mouse_state['pressed_at'] = None

    def hoverEnterEvent(self, event):
        """Handle mouse hover enter events

        Parameters
        ----------
        event : QtEvent
        """
        x = event.pos().x()
        y = event.pos().y()
        button = self._mouse_state['button']
        propagate = self._handle_event(('enter', button, int(event.modifiers())), x, y)
        if propagate:
            self.parent_class.hoverEnterEvent(self, event)
        else:
            event.accept()

    def hoverLeaveEvent(self, event):
        """Handle mouse hover enter events

        Parameters
        ----------
        event : QtEvent
        """
        x = event.pos().x()
        y = event.pos().y()
        button = self._mouse_state['button']
        propagate = self._handle_event(('leave', button, int(event.modifiers())), x, y)
        if propagate:
            self.parent_class.hoverLeaveEvent(self, event)
        else:
            event.accept()

    def wheelEvent(self, event):
        """Handle mouse hover enter events

        Parameters
        ----------
        event : QtEvent
        """
        delta = event.delta()
        button = self._mouse_state['button']
        propagate = self._handle_event(('wheel', button, int(event.modifiers())), delta)
        if propagate:
            self.parent_class.wheelEvent(self, event)
        else:
            event.accept()