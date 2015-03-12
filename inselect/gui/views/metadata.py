import re
from functools import partial

from PySide.QtGui import (QAbstractItemView, QSizePolicy, QScrollArea,
                          QWidget, QGroupBox, QLabel, QLineEdit, QComboBox,
                          QFormLayout, QVBoxLayout)
from PySide.QtCore import Qt

from inselect.lib.countries import COUNTRIES
from inselect.lib.languages import LANGUAGES
from inselect.lib.utils import debug_print

from inselect.gui.metadata_library import metadata_library
from inselect.gui.roles import MetadataRole
from inselect.gui.utils import relayout_widget


# The value that is displayed for a field when more than one box is selected
# and the items have more than one unique value for that field
_MULTIPLE_FIELD_VALUES = u'*'


class MetadataView(QAbstractItemView):
    """Metadata in a form
    """

    def __init__(self, parent=None):
        # This view is never made visible
        super(MetadataView, self).__init__()

        # List of metadata templates
        self._templates = self._create_templates_list()
        self._templates.activated.connect(self._template_changed)

        # A container for the controls
        self._form_container = FormContainer()

        # A scrollable container for the form
        self._form_scroll = QScrollArea(parent)
        self._form_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._form_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._form_scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._form_scroll.setWidget(self._form_container)

        # Make the controls fill the available horizontal space
        # http://qt-project.org/forums/viewthread/11012
        self._form_scroll.setWidgetResizable(True)

        self._create_controls()

        # List of templates is fixed at the top - form can be scrolled
        layout = QVBoxLayout()
        layout.addWidget(self._templates)
        layout.addWidget(self._form_scroll)

        # Top-level container for the list of templates and form
        self.widget = QWidget(parent)
        self.widget.setLayout(layout)

    def _create_templates_list(self):
        """Returns a QComboBox populated with metadata template names
        """
        c = QComboBox()
        select_index = 0
        for index, template in enumerate(metadata_library.library):
            c.addItem(template.name, index)
            if metadata_library.current == template.name:
                select_index = index
        c.setCurrentIndex(select_index)
        return c

    def _template_changed(self):
        """The user changed the template
        """
        debug_print('MetadataView._template_changed')

        # Save the user's choice
        metadata_library.set_current(self._templates.currentText())

        # Recreate controls
        self._create_controls()

        # Inform the model
        # TODO Should be a signal
        self.model().metadata_template_changed()

        self._populate_controls()

    def _populate_controls(self):
        """Populates the controls with metadata values in the selection
        """
        selected = self.selectionModel().selectedIndexes()

        # TODO Combos should indicate multiple and unrecognised values
        # Put values into the controls
        metadata = [i.data(MetadataRole) for i in selected]
        for field, control in self._form_container.controls.iteritems():
            values = {m.get(field,'') for m in metadata}
            control.selection_changed(selected, values)

    def _create_controls(self):
        """Creates controls for editing fields in the selected template
        """
        value = self._templates.itemData(self._templates.currentIndex())
        self._form_container.controls_from_template(metadata_library.current)

    def reset(self):
        """QAbstractItemView virtual
        """
        debug_print('MetadataView.reset')
        super(MetadataView, self).reset()

        # Clear the controls
        self._populate_controls()

    def selectionChanged(self, selected, deselected):
        """QAbstractItemView slot
        """
        debug_print('MetadataView.selectionChanged')
        self._populate_controls()


class FormContainer(QWidget):
    """A widget that holds metadata edit controls
    """

    # Set when field contains an invalid value
    STYLESHEET = """
    FieldEdit[invalid="true"] {
        background: pink;
    }

    ToggleWidgetLabel {
        text-decoration: none;
        font-weight: bold;
        color: black;
    }
    """
    def __init__(self, parent=None):
        super(FormContainer, self).__init__(parent)

        self.setStyleSheet(self.STYLESHEET)

        # Mapping { field name: control }
        self.controls = {}

    def controls_from_template(self, template):
        # TODO Remove existing controls

        # Create new controls and layout
        self.controls, layout = self._create_field_controls(template)

        relayout_widget(self, layout)

    def _new_group(self):
        # Returns a new layout
        l = QFormLayout()
        l.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        return l

    def _close_group(self, main_layout, group_name, group_layout):
        """Closes the the existing group
        """
        debug_print('FormContainer._close_group close group', group_name)

        # The widget that holds this group's controls
        controls_widget = QWidget()
        controls_widget.setLayout(group_layout)

        if group_name:
            # Group controls start out hidden
            controls_widget.setVisible(False)

            # The group box, which contains the label to toggle the controls
            # and the controls themselves
            group_box_layout = QVBoxLayout()
            group_box_layout.addWidget(ToggleWidgetLabel(group_name,
                                                         controls_widget))
            group_box_layout.addWidget(controls_widget)
            group_box = QGroupBox()
            group_box.setLayout(group_box_layout)

            # Add the group box to the main layout
            main_layout.addRow(group_box)
        else:
            # current group has no name and therefore no toggle group
            main_layout.addRow(controls_widget)

    def _create_field_controls(self, template):
        """Creates QWidgets for editing each field in the metadata template, and
        returns a dict { field name: control }
        """
        # Show controls stacked vertically
        main_layout = QFormLayout()
        main_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        # Mapping { field name: control }
        controls = {}

        group_layout = current_group = None

        # Create controls and group boxes
        for field in template.fields:
            if field.get('Group') != current_group or group_layout is None:
                # Either field belongs to a different group to the last item or
                # this is the first field.
                if group_layout:
                    self._close_group(main_layout, current_group, group_layout)
                group_layout = self._new_group()
                current_group = field.get('Group')

            # Create control for this field
            control = self._create_field_control(field, template)
            label = field.get('Label', field['Name'])
            if 'URI' in field:
                group_layout.addRow(URLLabel(field['URI'], label), control)
            else:
                group_layout.addRow(QLabel(label), control)
            controls[field['Name']] = control

        self._close_group(main_layout, current_group, group_layout)

        return controls, main_layout

    def _create_field_control(self, field, template):
        """Returns a QWidget for editing field, validated using template
        """
        if 'countryCode' == field['Name']:
            return CountryComboBox()
        elif 'language' == field['Name']:
            return LanguageComboBox()
        else:
            # Not using Qt's very restrictive QValidator scheme
            edit = FieldEdit(field['Name'], template)
            return edit


class ToggleWidgetLabel(QLabel):
    """A QLabel that, when clicked, toggles the visibility of a widget
    """
    def __init__(self, label, widget, parent=None, flags=0):
        super(ToggleWidgetLabel, self).__init__(label, parent, flags)
        self.widget = widget
        self.setCursor(Qt.PointingHandCursor)

    def mouseReleaseEvent(self, event):
        """QLabel virtual
        """
        self.toggle()

    def toggle(self):
        """Toggle the visible state of self.widget
        """
        visible = self.widget.isVisible()
        self.widget.setVisible(not visible)


class URLLabel(QLabel):
    """A label that displays a clickable URL in black.
    """

    HTML = '''<html><head><style type=text/css>
    a:link {{ color: black; text-decoration: underline;}}
    </style></head>
    <body><a href="{0}">{1}</a></body>
    </html>
    '''

    def __init__(self, url, label, parent=None, f=0):
        html = self.HTML.format(url, label)
        super(URLLabel, self).__init__(html, parent, f)
        self.setOpenExternalLinks(True)


class FieldEdit(QLineEdit):
    """Updates the relevant model field when _editing_finished is called.
    """

    def __init__(self, field, template, parent=None):
        super(FieldEdit, self).__init__(parent)

        self.editingFinished.connect(self._editing_finished)

        self.selected = None
        self.setEnabled(False)

        # The name of the field
        self._field = field

        # The metadata template
        self._template = template

        # If True there is more than one value of self._field among the selected
        # items and editing_finished() will update the model only if self.text()
        # is not self.multiple_values
        self.multiple_values = False

    def _editing_finished(self):
        """QLineEdit signal
        """
        debug_print('FieldEdit._editing_finished', self._field,
                    'modified' if self.isModified() else 'unmodified',
                    'valid' if self.is_valid() else 'invalid')
        if self.isModified():
            self.setModified(False)
            value = self.text().strip()
            if (not self.multiple_values or
                (self.multiple_values and _MULTIPLE_FIELD_VALUES != value)):
                for i in self.selected:
                    i.model().setData(i, {self._field : value}, MetadataRole)
            self.sync_background()

    def selection_changed(self, selected, values):
        """New items selected. Values should be the set of unique values of this
        field in selected.
        """
        if 1 < len(values):
            # Indicate that there is more than one value of field among
            # the selected items
            self.setText(_MULTIPLE_FIELD_VALUES)
            self.multiple_values = True
        elif 1 == len(values):
            # Show the single value common to the whole selection
            self.setText(values.pop())
            self.multiple_values = False
        else:
            # No items selected
            self.setText(u'')
            self.multiple_values = False

        self.selected = selected
        self.setEnabled(len(selected) > 0)
        self.sync_background()

    def sync_background(self):
        current, new = self.property("invalid"), not self.is_valid()
        if current != new:
            self.setProperty("invalid", new)
            # Annoying stuff that we need to do to get the control to refresh
            # http://qt-project.org/wiki/DynamicPropertiesAndStylesheets
            self.style().unpolish(self)
            self.style().polish(self)
            self.update()

    def is_valid(self):
        """True if this field contains either a valid value or
        _MULTIPLE_FIELD_VALUES
        """
        if not self.selected:
            return True

        value = self.text().strip()
        if self.multiple_values and _MULTIPLE_FIELD_VALUES == value:
            # Multiple values selected
            return True
        else:
            
            return self._template.validate_field(self._field, value)


class FieldComboBox(QComboBox):
    """Updates the relevant model field when setCurrentIndex is called.
    The list is populated with value, which should be an iterable of
    (text, userdata) tuples.
    """

    # TODO Prevent keypress from being propogated to application when list
    # is collapsed.

    def __init__(self, field, values=[], parent=None):
        super(FieldComboBox, self).__init__(parent)
        self.activated.connect(self._user_selected_item)
        self.selected = None
        self.setEnabled(False)

        # QComboBox's default behaviour is to set a minimum width that is large
        # enough to show the longest item in the list. This has the effect of
        # setting the minimum width of the entire form. Set a minimum number
        # of characters width to allow the QComboBox, and hence the form, to
        # shrink to a narrower width.
        self.setMinimumContentsLength(1)

        # The name of the field
        self._field = field

        # If True there is more than one value of self._field among the selected
        # items and editing_finished() will update the model only if self.text()
        # is not self.multiple_values
        self.multiple_values = False

        # Empty item at the top of the list
        self.addItem('', '')
        for text, userdata in values:
            self.addItem(text, userdata)

    def _user_selected_item(self):
        """The user changed the selected item
        """
        debug_print('FieldComboBox._user_selected_item', self._field)
        value = self.itemData(self.currentIndex())
        new = {self._field : value}
        for i in self.selected:
            i.model().setData(i, new, MetadataRole)

    def selection_changed(self, selected, values):
        """New items selected. Values should be the set of unique values of this
        field in selected.
        """
        if 1 < len(values):
            # Indicate that there is more than one value of field among
            # the selected items
            self.setCurrentIndex(0)
            self.multiple_values = True
        elif 1 == len(values):
            # Show the single value common to the whole selection
            self.setCurrentIndex(self.findData(values.pop()))
            self.multiple_values = False
        else:
            # No items selected
            self.setCurrentIndex(0)
            self.multiple_values = False

        self.selected = selected
        self.setEnabled(len(selected) > 0)


class CountryComboBox(FieldComboBox):
    """List of 2-digit country codes and country names. The
    countryCode field is updated.
    """

    # TODO Integrate with 'Choices' of metadata spec
    # TODO How to set country and countryCode as user changes selection

    def __init__(self, parent=None):
        display = u'{0} ({1})'
        codes = sorted(COUNTRIES.keys())
        values = ((display.format(code, COUNTRIES[code]), code) for code in codes)
        super(CountryComboBox, self).__init__('countryCode', values, parent)


class LanguageComboBox(FieldComboBox):
    """List of 2-digit language codes and localised language names. The
    language field is updated.
    """
    def __init__(self, parent=None):
        display = u'{0} ({1})'
        codes = sorted(LANGUAGES.keys())
        values = ((display.format(code, LANGUAGES[code]), code) for code in codes)
        super(LanguageComboBox, self).__init__('language', values, parent)
