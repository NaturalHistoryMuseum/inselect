from PySide import QtCore


class MouseHandler(object):
    """Mixin used to map mouse events to methods.

    This mixin uses the following event names: 'press', 'release', 'double-click', 'wheel', 'move', 'enter', 'leave'.
    The mouse state contains the following properties:
        button : str, None
            The current button state. One of 'left', 'right', 'middle', None
        pressed_at : tuple, None
            A tuple defining (x, y) where the button was pressed (if still pressed) or None
        delta : tuple
            A tuple definine (delta_x, delta_y) of the current mouse movement
        over : bool
            True if the mouse is over the current item, false if not
        modifier : int
            A Qt key modifier constant

    Example
    -------
    To use MouseEvents, you need to inherit from it and call it's initializer specifying the class which holds
    the default Mouse events implementation:

        class GraphicsView(MouseEvents, QtGui.QGraphicsView):
        def __init__(self, parent=None):
            QtGui.QGraphicsView.__init__(self, parent)
            MouseEvents.__init__(self, parent_class=QtGui.QGraphicsView)

    You can then add handlers for any combination of events and mouse state:

            self.add_mouse_handler(('move', {'button': 'middle'}), self.scroll_view, args=[True])
            self.add_mouse_handler(('wheel', {'button': None, 'modifier': QtCore.Qt.ControlModifier}), self.zoom)

    The functions will be called with event-specific arguments:
        def scroll_view(self, x, y):
            h = self.horizontalScrollBar()
            v = self.verticalScrollBar()
            delta = self.get_mouse_state('delta')
            h.setValue(h.value() + delta[0])
            v.setValue(v.value() + delta[1])

    Notes
    -----
    - The mixin implements Qt mouse events methods, so classes should not implement their own.
    - Some elements, such as elements derived from QtGraphicsItem, will not trigger mouse move
      events unless a button is pressed. To change that behaviour, you need to call
      `setAcceptHoverEvents` to True. Qt will then fire different events whether a button is
      pressed or not. The MouseEvents abstracts this behaviour - so you can rely on the event
      ('move', {'over': True}) to work in both instances.
    """
    def __init__(self, parent_class):
        self.parent_class = parent_class

        self._last_position = (0, 0)
        self._mouse_state = {
            'button': None,
            'pressed_at': None,
            'delta': (0, 0),
            'over': False,
            'modifier': QtCore.Qt.NoModifier
        }

        self._handlers = {}

    def add_mouse_handler(self, event, callback, delegate=False, args=None):
        """Add a new mouse handler

        Parameters
        ----------
        event : str, tuple
            see `_get_event`
        callback : function
            Function to call on event. If delegate is True, the function should return True to
            allow the event to propagate, False otherwise.
        delegate : bool
            If False (the default), events will not propagate when the handler is invoked.
            If True, the value of the callback function will determine whether events should
            propagate (True to propagate)
        args : list, None
            Additional arguments will be passed to the callback methods, *after* the event
            specific arguments.
        """
        (event, state) = self._get_event(event)
        if args is None:
            args = []
        if event not in self._handlers:
            self._handlers[event] = []
        self._handlers[event].append((callback, state, delegate, args))

    def get_mouse_state(self, prop=None):
        """Return the mouse state

        Parameters
        ----------
        prop : str, None
            The name of a property or None

        Returns
        -------
        object
            Either a given property (if prop is not None), or the whole mouse state object
        """
        if prop is None:
            return self._mouse_state
        else:
            return self._mouse_state[prop]

    def _get_event(self, event):
        """Return a (event, state) tuple for the given event

        Parameters
        ----------
        event : str, tuple
            May be an event name, a tuple defining (event, state) where:
                - event is one of 'press', 'release', 'double-click', 'wheel', 'move', 'enter', 'leave';
                - state is an object mapping mouse_state properties to values
                
        Returns
        -------
        tuple
            An (event, state) tuple
        """
        event_str = event
        state = {}
        if isinstance(event, (list, tuple)):
            event_str = event[0]
            if len(event) > 1:
                state = dict(event[1])
                if 'modifier' in state:
                    state['modifier'] = int(state['modifier'])

        return event_str, state

    def _handle_event(self, event, event_name, default_callback, args=None):
        """Handle an event by calling appropriate handlers

        Parameters
        ----------
        event : QtEvent
            The event that triggered the call
        event_name : str
            Event name. See `_get_event`
        default_callback : function
            Function to call for propagation
        args : list
            Additional arguments, that are passed to the callback function *before*
            the additional arguments defined when creating the handler.
        """
        # Get handlers
        try:
            handlers = self._handlers[event_name]
        except KeyError:
            default_callback(self, event)
            return
        # Set non-event specific mouse state
        self._mouse_state['modifier'] = int(event.modifiers())
        # Call handlers that match the state
        if args is None:
            args = []
        propagate = True
        for (callback, state, delegate, handler_args) in handlers:
            cancel = False
            for prop in state:
                if self._mouse_state[prop] != state[prop]:
                    cancel = True
                    break
            if cancel:
                continue
            r = callback(*(args + handler_args))
            if delegate:
                propagate = propagate & r
            else:
                propagate = False
        # Propagate or accept the event
        if propagate:
            default_callback(self, event)
        else:
            event.accept()

    def mousePressEvent(self, event):
        """Handle mouse press events

        Parameters
        ----------
        event : QtEvent
        """
        x = event.pos().x()
        y = event.pos().y()
        self._mouse_state['pressed_at'] = (x, y)
        if event.button() == QtCore.Qt.MidButton:
            self._mouse_state['button'] = 'middle'
        elif event.button() == QtCore.Qt.LeftButton:
            self._mouse_state['button'] = 'left'
        elif event.button() == QtCore.Qt.RightButton:
            self._mouse_state['button'] = 'right'

        self._handle_event(event, 'press', self.parent_class.mousePressEvent, args=[x, y])

    def mouseMoveEvent(self, event):
        """Handle mouse move events

        Parameters
        ----------
        event : QtEvent
        """
        x = event.pos().x()
        y = event.pos().y()
        self._mouse_state['delta'] = (self._last_position[0] - x, self._last_position[1] - y)
        self._handle_event(event, 'move', self.parent_class.mouseMoveEvent, args=[x, y])
        self._last_position = (x, y)

    def mouseReleaseEvent(self, event):
        """Handle mouse release events

        Parameters
        ----------
        event : QtEvent
        """
        x = event.pos().x()
        y = event.pos().y()
        self._handle_event(event, 'release', self.parent_class.mouseReleaseEvent, args=[x, y])
        self._mouse_state['button'] = None
        self._mouse_state['pressed_at'] = None

    def mouseDoubleClickEvent(self, event):
        """Handle mouse double click events

        Parameters
        ----------
        event : QtEvent
        """
        x = event.pos().x()
        y = event.pos().y()
        self._handle_event(event, 'double-click', self.parent_class.mouseDoubleClickEvent, args=[x, y])

    def hoverEnterEvent(self, event):
        """Handle mouse hover enter events

        Parameters
        ----------
        event : QtEvent
        """
        x = event.pos().x()
        y = event.pos().y()
        self._mouse_state['over'] = True
        self._handle_event(event, 'enter', self.parent_class.hoverEnterEvent, args=[x, y])

    def hoverMoveEvent(self, event):
        """Handle hoverMoveEvent

        Parameters
        ----------
        event : QtEvent
        """
        x = event.pos().x()
        y = event.pos().y()
        over = self._mouse_state['over']
        self._mouse_state['over'] = True
        self._mouse_state['delta'] = (self._last_position[0] - x, self._last_position[1] - y)
        self._handle_event(event, 'move', self.parent_class.hoverMoveEvent, args=[x, y])
        self._last_position = (x, y)
        self._mouse_state['over'] = over

    def hoverLeaveEvent(self, event):
        """Handle mouse hover enter events

        Parameters
        ----------
        event : QtEvent
        """
        x = event.pos().x()
        y = event.pos().y()
        self._mouse_state['over'] = False
        self._handle_event(event, 'leave', self.parent_class.hoverLeaveEvent, args=[x, y])

    def wheelEvent(self, event):
        """Handle mouse hover enter events

        Parameters
        ----------
        event : QtEvent
        """
        delta = event.delta()
        self._handle_event(event, 'wheel', self.parent_class.wheelEvent, args=[delta])
