from functools import partial

from qtpy.QtWidgets import QApplication, QMessageBox


def copy_to_clipboard(text):
    QApplication.clipboard().setText(text)


def copy_details_box(icon, title, text, details):
    """Shows a QMessageBox with a detail box and a 'Copy details' button
    """
    box = QMessageBox(icon, title, text)
    box.setDetailedText(details)
    copy_button = box.addButton('Copy details', QMessageBox.HelpRole)

    # QMessageBox connects the clicked signal of the new button to a close
    # action - disconnect this and connect to copy_to_clipboard
    copy_button.clicked.disconnect()
    copy_button.clicked.connect(partial(copy_to_clipboard, details))
    box.addButton('OK', QMessageBox.AcceptRole)
    return box.exec_()
