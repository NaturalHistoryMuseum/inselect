class Plugin(object):
    """Base class for plugins.
    """
    # TODO LH Config UI and settings

    def __init__(self, document, parent):
        """document - an instance of InselectDocument
        parent - a QMainWindow
        """
        raise NotImplementedError('name')

    @classmethod
    def name(cls):
        """Name of the plugin
        """
        raise NotImplementedError('name')

    @classmethod
    def description(cls):
        """A description of the effect of running this plugin.
        """
        return None

    @classmethod
    def icon(cls):
        """A PySide.QtGui.QIcon or None
        """
        return None

    def proceed(self):
        """If False is returned, the plugin is not run. If True is returned,
        the plugin is run in its own thread.
        """
        return True

    def __call__(self, progress):
        """Executes the plugin
        """
        raise NotImplementedError('__call__')
