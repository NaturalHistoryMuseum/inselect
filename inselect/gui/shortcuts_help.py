"""Dialog showing a list of shortcuts
"""
from PySide.QtCore import Qt, QSettings
from PySide.QtGui import (QCheckBox, QDialog, QGridLayout, QHBoxLayout, QLabel,
                          QPushButton, QSizePolicy, QVBoxLayout, QWidget)


from inselect.gui.utils import HorizontalLine, VerticalLine
from inselect.gui.prompts import format_action_shortcuts, BOXES_VIEW_SHORTCUTS


class HeaderLabel(QLabel):
    pass


def _new_panel():
    """Returns a tuple (QWidget, QGridLayout)
    """
    panel = QWidget()
    panel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    layout = QGridLayout(panel)
    return panel, layout


def _add_header(layout, text):
    """Adds to layout a HeaderLabel containing text
    """
    row = layout.rowCount()
    layout.addWidget(HeaderLabel(text), row, 0, 1, 2)


def _add_hline(layout, row_minimum_height=20):
    """Adds a HorizontalLine to layout
    """
    row = layout.rowCount()
    layout.addWidget(HorizontalLine(), row, 0, 1, 2)
    layout.setRowMinimumHeight(row, row_minimum_height)


def _add_row(layout, action):
    """Adds to layout the text and shortcuts for action
    """
    row = layout.rowCount()
    layout.addWidget(QLabel(format_action_shortcuts(action)), row, 0)
    layout.addWidget(QLabel(action.iconText()), row, 1)


def _column1(main_window):
    """Returns a QWidget of shortcuts
    """
    panel, layout = _new_panel()

    _add_header(layout, 'File')
    _add_row(layout, main_window.open_action)
    _add_row(layout, main_window.save_action)
    _add_row(layout, main_window.close_action)
    _add_row(layout, main_window.exit_action)

    _add_hline(layout)
    _add_header(layout, 'Selection')
    _add_row(layout, main_window.next_box_action)
    _add_row(layout, main_window.previous_box_action)
    _add_row(layout, main_window.select_all_action)
    _add_row(layout, main_window.select_none_action)
    _add_row(layout, main_window.next_box_action)
    _add_row(layout, main_window.previous_box_action)
    _add_row(layout, main_window.select_by_size_larger_action)
    _add_row(layout, main_window.select_by_size_smaller_action)

    _add_hline(layout)
    _add_header(layout, 'Edit')
    _add_row(layout, main_window.delete_action)
    _add_row(layout, main_window.rotate_clockwise_action)
    _add_row(layout, main_window.rotate_counter_clockwise_action)

    return panel


def _column2(main_window):
    """Returns a QWidget of shortcuts
    """
    panel, layout = _new_panel()

    _add_header(layout, 'Tab navigation')
    _add_row(layout, main_window.boxes_view_action)
    _add_row(layout, main_window.objects_view_action)
    _add_row(layout, main_window.previous_tab_action)
    _add_row(layout, main_window.next_tab_action)

    _add_hline(layout)
    _add_header(layout, 'Boxes tab')
    _add_row(layout, main_window.zoom_in_action)
    _add_row(layout, main_window.zoom_out_action)
    _add_row(layout, main_window.zoom_home_action)
    _add_row(layout, main_window.zoom_to_selection_action)
    # TODO LH zoom using trackpad / wheel

    for text, shortcut in BOXES_VIEW_SHORTCUTS:
        row = layout.rowCount()
        layout.addWidget(QLabel(shortcut), row, 0)
        layout.addWidget(QLabel(text), row, 1)

    _add_hline(layout)
    _add_header(layout, 'Objects tab')
    _add_row(layout, main_window.view_object.grid_action)
    _add_row(layout, main_window.view_object.expanded_action)

    return panel


_KEY = 'show_shortcuts_at_startup'


def _show_shortcuts_at_startup():
    """True if shortcuts should be shown at startup; default True.
    """
    # Key holds an integer
    return 1 == QSettings().value(_KEY, 1)


def show_shortcuts(main_window):
    """Shows a modal QDialog of shortcuts
    """
    dialog = QDialog(main_window)
    dialog.setWindowTitle('Inselect')

    hlayout = QHBoxLayout()
    hlayout.addWidget(_column1(main_window), alignment=Qt.AlignTop)
    hlayout.addWidget(VerticalLine())
    hlayout.addWidget(_column2(main_window), alignment=Qt.AlignTop)

    vlayout = QVBoxLayout()
    vlayout.addWidget(
        HeaderLabel('Shortcuts and controls'),
        alignment=Qt.AlignHCenter | Qt.AlignTop
    )
    vlayout.addWidget(HorizontalLine())
    vlayout.addLayout(hlayout)

    show_at_startup = QCheckBox('Show this help the next time Inselect starts')
    show_at_startup.setChecked(_show_shortcuts_at_startup())
    vlayout.addWidget(show_at_startup, alignment=Qt.AlignLeft)

    prompt = ("Show this help at any time by pressing '{0}' or by selecting "
              "'{1}' from the Help menu.")
    vlayout.addWidget(QLabel(prompt.format(
        format_action_shortcuts(main_window.show_shortcuts_action),
        main_window.show_shortcuts_action.iconText()
    )))

    close = QPushButton('Close')
    close.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    close.setDefault(True)
    close.clicked.connect(dialog.close)
    vlayout.addWidget(close, alignment=Qt.AlignHCenter)

    dialog.setLayout(vlayout)

    # TODO This belongs in the app's stylesheet but it wasn't respected
    # when I tried it
    dialog.setStyleSheet("""
    HeaderLabel {
        font-weight: bold;
        font-size: 16px;
    }
    """)
    dialog.exec_()

    QSettings().setValue(_KEY, 1 if show_at_startup.isChecked() else 0)


def show_shortcuts_post_startup(main_window):
    """Shows a modal QDialog of shortcuts, if 'show_shortcuts_at_startup' is
    selected.
    """
    # Key holds an integer
    if _show_shortcuts_at_startup():
        show_shortcuts(main_window)
