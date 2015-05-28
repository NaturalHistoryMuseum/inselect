class Plugin(object):
    """Base class for plugins.

    The __init__ method of derived classes should accept two arguments:
        document - an instance of InselectDocument
        parent - a QMainWindow

    Derived classes should contain
        NAME - a string
        DESCRIPTION - a string

    Derived classes can contain
        icon() - a classmethod that returns a QIcon
    """

    # TODO LH Config UI and settings

    def can_be_run(self):
        """If False is returned, the plugin is not run. If True is returned,
        the plugin is run in its own thread.
        """
        return True

    def __call__(self, progress):
        """Executes the plugin
        """
        raise NotImplementedError('__call__')
