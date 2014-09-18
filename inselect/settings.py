from PySide import QtCore, QtGui
from PySide.QtCore import QSettings
from inselect.lib import validators


# Define the available settings. Each entry associates the internal setting name to a dictionary defining:
# label : str, required
#     Label as shown to the user.
# description : str, optional
#     Description as shown to the user. This is required if editable is True.
# editable : bool, optional
#     True if the setting can be changed by the user.
# type : str, optional
#     One of 'int', 'float', 'bool', 'list' or 'str' (default).
# validate : function, optional
#     Validation function, returns a boolean.
# default : object, required
#     Default value for the setting.
_settings = {
    'annotation_fields': {
        'label': "Annotation fields",
        'description': 'Comma separated list of fields available in the annotation editor',
        'editable': True,
        'type': 'list',
        'validate': validators.not_empty,
        'default': ['Specimen Number', 'Current Taxon Name', 'Location in Collection']
    },
    'export_template': {
        'label': 'Export file name',
        'description': 'Template for image export file names. You can use any of the annotation fields<br/> between {'
                       'curly brackets}. To insert plain curly brackets, double them.',
        'editable': True,
        'type': 'str',
        'validate': validators.validate_export_template,
        'default': 'BMNHE_{Specimen Number}{Current Taxon Name}'
    }
}


def init():
    """Setup the default values for the QSettings object"""
    qsettings = QSettings('NHM', 'Inselect')
    for name in _settings:
        if not qsettings.contains(name):
            qsettings.setValue(name, _settings[name]['default'])


def open_settings_dialog():
    """Open the settings dialog"""
    dialog = _SettingsDialog()
    dialog.exec_()


def reset(name=None):
    """Reset settings to default values

    If setting is None, then all settings are reset.

    Parameters
    ----------
    name : str, None
        The setting to reset, or None
    """
    qsettings = QSettings('NHM', 'Inselect')
    if name:
        qsettings.setValue(name, _settings[name]['default'])
    else:
        qsettings.clear()
        init()


class _SettingsDialog(QtGui.QDialog):
    """ Settings Dialog """
    _description_template = """
        <html><head/><body><p><span style=" font-size:10pt; font-style:italic;">{content}</span></p></body></html>
    """
    _error_template = """
        <html><head/><body><p><span style=" font-size:12pt; color: #F00;">{content}</span></p></body></html>
    """

    def __init__(self, parent=None):
        super(_SettingsDialog, self).__init__(parent)
        qsettings = QSettings('NHM', 'Inselect')

        # Set up the UI
        self.edits = {}
        self.descriptions = {}
        self.setup_dialog()
        for name in _settings:
            schema = _settings[name]
            value = qsettings.value(name)
            if 'editable' in schema and schema['editable']:
                if 'type' in schema:
                    if schema['type'] == 'bool':
                        value = 'True' if value else 'False'
                    elif schema['type'] == 'list':
                        if isinstance(value, list):
                            value = ', '.join(value)
                        else:
                            value = ''
                    else:
                        value = str(value)
                self.add_dialog_row(name, schema['label'], schema['description'], str(value))

        # Connect signals
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL("accepted()"), self.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL("rejected()"), self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def accept(self):
        """Callback invoked when the user clicks on Ok"""
        qsettings = QSettings('NHM', 'Inselect')
        failed = False
        for name in self.edits:
            schema = _settings[name]
            value = self.edits[name].text().strip()
            if 'type' in schema:
                if schema['type'] == 'int':
                    value = int(value)
                elif schema['type'] == 'float':
                    value = float(value)
                elif schema['type'] == 'bool':
                    value = value.lower() in ['true', 'on', '1', 'yes']
                elif schema['type'] == 'list':
                    if len(value) == 0:
                        value = []
                    else:
                        value = [f.strip() for f in value.split(',')]
            if 'validate' in schema:
                try:
                    schema['validate'](value)
                except validators.ValidationError as e:
                    failed = True
                    error = str(e).format(label=schema['label'])
                    self.descriptions[name].setText(self._error_template.format(content=error))
                else:
                    self.descriptions[name].setText(self._description_template.format(content=schema['description']))
                    qsettings.setValue(name, value)
            else:
                    qsettings.setValue(name, value)
        if not failed:
            super(_SettingsDialog, self).accept()

    def setup_dialog(self):
        """Sets up the frame of the settings box"""
        grid_layout = QtGui.QGridLayout(self)
        self.button_box = QtGui.QDialogButtonBox(self)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        grid_layout.addWidget(self.button_box, 1, 0, 1, 1)
        scroll_area = QtGui.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self.row_parent = QtGui.QWidget()
        self.row_parent.setGeometry(QtCore.QRect(0, 0, 593, 563))
        self.row_container = QtGui.QVBoxLayout(self.row_parent)
        scroll_area.setWidget(self.row_parent)
        grid_layout.addWidget(scroll_area, 0, 0, 1, 1)

    def add_dialog_row(self, name, label, description, value):
        """Add a row to the settings dialog

        Parameters
        ----------
        name : str
            Name of the setting
        label : str
            Label of the setting
        description : str
            Description of the setting
        value : str
            Value of the setting
        """
        # Create the row
        group_box = QtGui.QGroupBox(self.row_parent)
        vertical_layout = QtGui.QVBoxLayout(group_box)
        group_box_2 = QtGui.QGroupBox(group_box)
        horizontal_layout = QtGui.QHBoxLayout(group_box_2)
        label_item = QtGui.QLabel(group_box_2)
        horizontal_layout.addWidget(label_item)
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        line_edit = QtGui.QLineEdit(group_box_2)
        horizontal_layout.addWidget(line_edit)
        vertical_layout.addWidget(group_box_2)
        description_label = QtGui.QLabel(group_box)
        description_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        vertical_layout.addWidget(description_label)
        self.row_container.addWidget(group_box)
        # Set values
        label_item.setText(label)
        description_label.setText(self._description_template.format(content=description))
        line_edit.setText(value)
        # Keep track
        self.edits[name] = line_edit
        self.descriptions[name] = description_label