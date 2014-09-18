from PySide import QtCore


class KeyHandler(object):
    """ Mixin used to map key combinations to methods.

    The mixin implements the Qt keyPressEvent method, so classes should not implement their own.
    """
    def __init__(self, parent_class):
        self._handlers = {}
        self._parent_class = parent_class

    def add_key_handler(self, key, callback, args=None):
        """Add a new key handler

        Parameters
        ----------
        key : int, tuple
            Either a key constant, or a tuple defining a modifier constant and a key constant
        callback : function
            Function to call on key press
        args : List
            Arguments will be passed to the callback method
        """
        (modifier, key_code) = self._get_key_code(key)
        if modifier not in self._handlers:
            self._handlers[modifier] = {}
        if key_code not in self._handlers[modifier]:
            self._handlers[modifier][key_code] = []
        if args is None:
            args = []
        self._handlers[modifier][key_code].append((callback, args))

    def remove_key_handlers(self, key):
        """Remove all key handlers associated with the given key

        Parameters
        ----------
        key : int, tuple
            Either a key constant, or a tuple defining a modifier constant and a key constant.
        """
        (modifier, key_code) = self._get_key_code(key)
        try:
            del self._handlers[modifier][key_code]
        except (AttributeError, KeyError):
            pass

    def _get_key_code(self, key):
        """Return a (modifier, key code) tupple for the given key

        Parameters
        ----------
        key : int, tuple
            Either a key constant, or a tuple defining a modifier constant and a key constant

        Returns
        -------
        tuple
            A (modifier, key code) tuple
        """
        if isinstance(key, (list, tuple)):
            return int(key[0]), int(key[1])
        else:
            return int(QtCore.Qt.NoModifier), int(key)

    def keyPressEvent(self, event):
        """Handle Qt keyPressEvent event

        Call the appropriate method for the key event

        Parameters
        ----------
        event : QtEvent
        """
        try:
            handlers = self._handlers[int(event.modifiers())][int(event.key())]
        except (AttributeError, KeyError):
            self._parent_class.keyPressEvent(self, event)
            return
        for (callback, args) in handlers:
            callback(*args)