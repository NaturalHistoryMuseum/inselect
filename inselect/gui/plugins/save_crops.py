from inselect.lib.utils import debug_print

from .plugin import Plugin


class SaveCropsPlugin(Plugin):
    """Saves images cropped from the full-resoution scan
    """
    @classmethod
    def name(cls):
        """Name of the plugin
        """
        return 'Save crops'

    @classmethod
    def prompt(cls):
        """A description of the effect of running this plugin.
        """
        return ("Will save images cropped from the full-resoution scan.")

    def __call__(self, document, progress):
        """
        """
        debug_print('SaveCropsPlugin.__call__')

        progress('Loading full-resolution scanned image')
        document.scanned.array

        document.save_crops(progress)

        debug_print('SaveCropsPlugin.__call__ exiting')

