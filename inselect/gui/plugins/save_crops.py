from inselect.lib.utils import debug_print

from .plugin import Plugin


class SaveCropsPlugin(Plugin):
    """Saves images cropped from the full-resoution scan
    """
    def __init__(self, document, parent):
        self.document = document

    @classmethod
    def name(cls):
        """Name of the plugin
        """
        return 'Save crops'

    @classmethod
    def description(cls):
        """A description of the effect of running this plugin.
        """
        return ("Will save images cropped from the full-resoution scan.")

    def __call__(self, progress):
        """
        """
        debug_print('SaveCropsPlugin.__call__')

        progress('Loading full-resolution scanned image')
        self.document.scanned.array

        self.document.save_crops(progress)

        debug_print('SaveCropsPlugin.__call__ exiting')

