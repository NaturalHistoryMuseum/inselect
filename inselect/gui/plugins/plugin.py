class Plugin(object):
    """Base class for plugins.
    """
    # TODO LH Config UI and settings

    @classmethod
    def name(cls):
        """Name of the plugin
        """
        raise NotImplementedError('name')

    @classmethod
    def prompt(cls):
        """A description of the effect of running this plugin.
        """
        return None

    @classmethod
    def icon(cls):
        """A PySide.QtGui.QIcon or None
        """
        return None

    def __call__(self, document, progress):
        """Executes the plugin
        """
        raise NotImplementedError('__call__')
