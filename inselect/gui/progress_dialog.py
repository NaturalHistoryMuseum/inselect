from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressDialog

from inselect.lib.utils import debug_print


class ProgressDialog(QProgressDialog):
    """A QProgressDialog that does not hide itself when cancel is pressed
    """
    def __init__(self, parent=0, f=Qt.WindowFlags(0)):
        super(ProgressDialog, self).__init__(parent, f)

        # The QProgressDialog::cancel() slot hides the dialog - disconnect it
        # and connect self.user_cancelled.
        self.canceled.disconnect()
        self.canceled.connect(self.user_cancelled)
        self._was_cancelled = False

    def user_cancelled(self):
        """Slot
        """
        debug_print('ProgressDialog.cancel')
        self._was_cancelled = True
        self.setLabelText('Cancelling...')

    @property
    def was_cancelled(self):
        """True if the user has pressed cancel. False otherwise.
        """
        return self._was_cancelled

    def wasCanceled(self):
        """QProgressDialog function
        """
        # TODO LH Not a virtual function - is it OK to provide this
        # implementation?
        return self.was_cancelled
