from itertools import izip, repeat

from PySide import QtGui
from PySide.QtGui import (QAbstractItemView, QSizePolicy, QScrollArea,
                          QWidget, QGroupBox, QLabel, QLineEdit, QComboBox,
                          QFormLayout, QVBoxLayout)
from PySide.QtCore import Qt

from inselect.lib.countries import COUNTRIES
from inselect.lib.languages import LANGUAGES
from inselect.lib.utils import debug_print

from inselect.gui.colours import colour_scheme_choice
from inselect.gui.popup_panel import PopupPanel
from inselect.gui.roles import MetadataRole
from inselect.gui.toggle_widget_label import ToggleWidgetLabel
from inselect.gui.utils import relayout_widget
from inselect.gui.user_template_choice import user_template_choice
from inselect.gui.user_template_popup_button import UserTemplatePopupButton


# The value that is displayed for a field when more than one box is selected
# and the items have more than one unique value for that field
_MULTIPLE_FIELD_VALUES = '*'


class MetadataView(QAbstractItemView):
    """Metadata in a form
    """

    def __init__(self, parent=None):
        # This view is never made visible
        super(MetadataView, self).__init__()

        user_template_choice().template_changed.connect(self.refresh_user_template)

        self.popup_button = UserTemplatePopupButton()

        # A container for the controls
        self._form_container = FormContainer()
        self._create_controls()

        # Popup buttom above controls
        layout = QVBoxLayout()
        layout.addWidget(self.popup_button)
        layout.addWidget(self._form_container)

        # Container for the popup and form
        container = QWidget()
        container.setLayout(layout)

        # Widget containing toggle label and container
        self.widget = PopupPanel('Metadata', container, parent)

    def refresh_user_template(self):
        "Refreshes the UI with the currently selected UserTemplate"
        self._create_controls()
        self._populate_controls()

    def _populate_controls(self):
        "Populates the controls with metadata values in the selection"
        selected = self.selectionModel().selectedIndexes()

        if 0 == len(selected):
            # No boxes selected
            for control in self._form_container.controls.iterkeys():
                control.clear_selection()
                control.setEnabled(False)
        else:
            metadata = [i.data(MetadataRole) for i in selected]
            for control, field in self._form_container.controls.iteritems():
                control.setEnabled(True)
                values = set(m.get(field) for m in metadata)
                if 1 < len(values):
                    # Indicate multiple values
                    control.set_multiple(selected)
                elif None in values:
                    # Indicate no value selected
                    control.clear_value(selected)
                else:
                    # Put the value into the controls
                    control.set_value(selected, values.pop())

    def _create_controls(self):
        "Creates controls for editing fields in the selected template"
        self._form_container.controls_from_template(user_template_choice().current)

    def reset(self):
        "QAbstractItemView virtual"
        debug_print('MetadataView.reset')
        super(MetadataView, self).reset()

        # Clear the controls
        self._populate_controls()

    def selectionChanged(self, selected, deselected):
        "QAbstractItemView slot"
        debug_print('MetadataView.selectionChanged')

        # If one of our controls has focus, update the model before refreshing
        # the UI
        if QtGui.qApp.focusWidget() in self._form_container.controls:
            QtGui.qApp.focusWidget().update_model()
        self._populate_controls()


class FormContainer(QWidget):
    """A widget that holds metadata edit controls
    """

    # Set when field contains an invalid value
    STYLESHEET = """
    FieldEdit[invalid="true"] {{
        background: {InvalidFill};
    }}

    FieldComboBox[invalid="true"] {{
        background: {InvalidFill};
    }}

    ToggleWidgetLabel {{
        text-decoration: none;
        font-weight: bold;
        color: black;
    }}
    """

    # TODO LH Text colour to come from system

    def __init__(self, parent=None):
        super(FormContainer, self).__init__(parent)

        stylesheet = self.STYLESHEET.format(**{
            k: v.name()
            for k, v in colour_scheme_choice().current['Colours'].iteritems()
            if v
        })

        self.setStyleSheet(stylesheet)

        # Mapping { control: field name }
        self.controls = {}

    def controls_from_template(self, template):
        "Create new controls and layout"
        self.controls, layout = self._create_field_controls(template)

        relayout_widget(self, layout)

    def _new_group(self):
        """Returns a new layout, used during controls creation
        """
        layout = QFormLayout()
        layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        return layout

    def _close_group(self, main_layout, group_name, group_layout):
        """Closes the the existing group, used during controls creation
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
            group_box_layout.setContentsMargins(
                0,  # left
                0,  # top
                0,  # right
                0   # bottom
            )
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
        main_layout.setContentsMargins(
            0,  # left
            0,  # top
            0,  # right
            0   # bottom
        )

        # Mapping { control, field name }
        controls = {}

        group_layout = current_group = None

        # Create controls and group boxes
        for field in template.fields:
            if field.group != current_group or group_layout is None:
                # Either field belongs to a different group to the last item or
                # this is the first field.
                if group_layout:
                    self._close_group(main_layout, current_group, group_layout)
                group_layout = self._new_group()
                current_group = field.group

            # Create control for this field
            control = self._create_field_control(field, template)
            if field.uri:
                group_layout.addRow(URLLabel(field.uri, field.label), control)
            else:
                group_layout.addRow(QLabel(field.label), control)
            controls[control] = field.name

        self._close_group(main_layout, current_group, group_layout)

        return controls, main_layout

    def _create_field_control(self, field, template):
        """Returns a QWidget for editing field, validated using template
        """
        if 'countryCode' == field.name:
            return CountryComboBox(template)
        elif 'language' == field.name:
            return LanguageComboBox(template)
        elif field.choices:
            combo = ChoicesFieldComboBox(field.name, template,
                                         labels=field.choices)
            return combo
        elif field.choices_with_data:
            choices = field.choices_with_data
            combo = ChoicesWithDataFieldComboBox(field.name, template,
                                                 labels=choices.iterkeys(),
                                                 values=choices.itervalues())
            return combo
        else:
            # Not using Qt's very restrictive QValidator scheme
            edit = FieldEdit(field.name, template)
            return edit


class URLLabel(QLabel):
    """A label that displays a clickable URL in black.
    """

    # TODO LH Text colour to come from system
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

        self.textEdited.connect(self._text_edited)

        self.selected = None

        # The name of the field
        self._field = field

        # The metadata template
        self._template = template

        # If True there is more than one value of self._field among the selected
        # items and editing_finished() will update the model only if self.text()
        # is not self.multiple_values
        self.multiple_values = False

    def __repr__(self):
        return u'<FieldEdit [{0}]>'.format(self._field)

    def __str__(self):
        return u'FieldEdit [{0}]'.format(self._field)

    def _text_edited(self, text):
        """QLineEdit signal
        """
        self.update_model()

    def update_model(self):
        """Updates the model
        """
        debug_print('FieldEdit.update_model', self._field,
                    'modified' if self.isModified() else 'unmodified',
                    'valid' if self.is_valid() else 'invalid')
        if self.isModified():
            self.setModified(False)
            value = self.text()
            if (not self.multiple_values or
                    (self.multiple_values and _MULTIPLE_FIELD_VALUES != value)):
                new = {self._field: value}
                for i in self.selected:
                    i.model().setData(i, new, MetadataRole)
            self.sync_background()

    def _update(self, selected, multiple, value):
        self.selected = selected
        self.multiple_values = multiple
        self.setText(value)
        self.sync_background()

    def clear_selection(self):
        self._update(None, False, '')

    def clear_value(self, selected):
        self._update(selected, False, '')

    def set_multiple(self, selected):
        self._update(selected, True, _MULTIPLE_FIELD_VALUES)

    def set_value(self, selected, value):
        # Show the single value common to the whole selection
        self._update(selected, False, value)

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

        value = self.text()
        if self.multiple_values and _MULTIPLE_FIELD_VALUES == value:
            # Multiple values selected
            return True
        else:
            return self._template.validate_field(self._field, value)


class FieldComboBox(QComboBox):
    """A base class for controls that contain lists of items.

    The first item is
    * empty
    * when the selection contains multiple values of this field,
      _MULTIPLE_FIELD_VALUES
    * a value that is not in the list, shown as invalid

    Derived classes should implement _data_for_model and _index_of_data
    """

    # TODO Prevent keypress from being propogated to application when list
    # is collapsed.

    def __init__(self, field, template, labels, values, parent):
        """labels - an iterable of strings
        values - an iterable of len(labels)
        """
        super(FieldComboBox, self).__init__(parent)
        self.activated.connect(self._user_selected_item)

        self.selected = None

        # QComboBox's default behaviour is to set a minimum width that is large
        # enough to show the longest item in the list. This has the effect of
        # setting the minimum width of the entire form. Set a minimum number
        # of characters width to allow the QComboBox, and hence the form, to
        # shrink to a narrower width.
        self.setMinimumContentsLength(1)

        self._template = template

        # The name of the field
        self._field = field

        # Empty item at the top of the list
        self.addItem('')

        for label, value in izip(labels, values):
            self.addItem(label, value)

        # True if selection contains a single non-empty value that is not in the
        # list of options
        self.unrecognised_value = False

    def __repr__(self):
        return u'<FieldComboBox [{0}]>'.format(self._field)

    def __str__(self):
        return u'FieldComboBox [{0}]'.format(self._field)

    @property
    def is_multiple(self):
        """True if multiple values are selected
        """
        return (_MULTIPLE_FIELD_VALUES == self.currentText() and
                0 == self.currentIndex())

    def _ensure_multiple_choice(self):
        """Ensures that the 'multiple values' choice is in the list
        """
        if _MULTIPLE_FIELD_VALUES != self.itemText(0):
            self.insertItem(0, _MULTIPLE_FIELD_VALUES)

    def _remove_multiple_choice(self):
        """Removes the 'multiple values' choice from the list
        """
        if _MULTIPLE_FIELD_VALUES == self.itemText(0):
            self.removeItem(0)

    @property
    def is_unrecognised_value(self):
        """True if an unrecognised value is visible
        """
        return self.unrecognised_value and 0 == self.currentIndex()

    def _insert_unrecognised_value(self, value):
        """Ensures that the unrecognised value is in the list
        """
        self.unrecognised_value = True
        self.insertItem(0, value)
        self.setCurrentIndex(0)

    def _remove_unrecognised_value(self):
        """Removes the unrecognised value from the list
        """
        if self.unrecognised_value:
            self.removeItem(0)
            self.unrecognised_value = False

    def _user_selected_item(self):
        """The user changed the selected item
        """
        self.update_model()

    def _update(self, selected, multiple, value):
        self.selected = selected
        if multiple:
            self._remove_unrecognised_value()
            self._ensure_multiple_choice()
            self.setCurrentIndex(0)
        else:
            self._remove_multiple_choice()
            self._remove_unrecognised_value()
            if value:
                index = self._index_of_data(value)
                if -1 == index:
                    self._insert_unrecognised_value(value)
                else:
                    self.setCurrentIndex(index)
            else:
                self.setCurrentIndex(0)
        self.sync_background()

    def clear_selection(self):
        self._update(None, False, None)

    def clear_value(self, selected):
        self._update(selected, False, None)

    def set_multiple(self, selected):
        self._update(selected, True, None)

    def set_value(self, selected, value):
        # Show the single value common to the whole selection
        self._update(selected, False, value)

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
        elif self.is_multiple:
            # Multiple values selected
            return True
        elif self.is_unrecognised_value:
            # A single value that is not in the list of options
            return False
        else:
            return self._template.validate_field(self._field,
                                                 self._data_for_model())

    def update_model(self):
        debug_print('ChoicesWithDataFieldComboBox.update_model', self._field)
        if not self.is_multiple and not self.is_unrecognised_value:
            # Update the selected items with the user's choice
            new = {self._field: self._data_for_model()}
            for i in self.selected:
                i.model().setData(i, new, MetadataRole)
            self.sync_background()

            # The user may have altered the choice from multiple to a value
            self._remove_multiple_choice()

            # The user may have altered the choice from unrecognised to a value
            self._remove_unrecognised_value()

    def _data_for_model(self):
        """Returns a value with which to update the model
        """
        raise NotImplemented('_data_for_model')

    def _index_of_data(self, data):
        """Returns the index of 'data' or -1 if data is not in the combo
        """

        raise NotImplemented('_data_from_model')


class ChoicesFieldComboBox(FieldComboBox):
    """A list of labels
    """
    def __init__(self, field, template, labels, parent=None):
        super(ChoicesFieldComboBox, self).__init__(field, template, labels,
                                                   repeat(None), parent)

    def _data_for_model(self):
        return self.currentText()

    def _index_of_data(self, value):
        # Show the single value common to the whole selection
        return self.findText(value)


class ChoicesWithDataFieldComboBox(FieldComboBox):
    """A list of labels with associated data
    """
    def __init__(self, field, template, labels, values, parent=None):
        super(ChoicesWithDataFieldComboBox, self).__init__(field, template,
                                                           labels, values,
                                                           parent)

    def _data_for_model(self):
        return self.currentText()

    def _index_of_data(self, value):
        # Show the single value common to the whole selection
        return self.findText(value)


class CountryComboBox(FieldComboBox):
    """List of 2-digit country codes and country names. The
    countryCode field is updated.
    """

    # TODO Integrate with 'Choices' of metadata spec
    # TODO How to set country and countryCode as user changes selection

    def __init__(self, template, parent=None):
        display = u'{0} ({1})'
        codes = sorted(COUNTRIES.keys())
        labels = (display.format(code, COUNTRIES[code]) for code in codes)
        super(CountryComboBox, self).__init__('countryCode', template, labels, codes, parent)

    def _data_for_model(self):
        return self.itemData(self.currentIndex())

    def _index_of_data(self, value):
        # Show the single value common to the whole selection
        return self.findData(value)


class LanguageComboBox(FieldComboBox):
    """List of 2-digit language codes and localised language names. The
    language field is updated.
    """
    def __init__(self, template, parent=None):
        display = u'{0} ({1})'
        codes = sorted(LANGUAGES.keys())
        labels = (display.format(code, LANGUAGES[code]) for code in codes)
        super(LanguageComboBox, self).__init__('language', template, labels, codes, parent)

    def _data_for_model(self):
        return self.itemData(self.currentIndex())

    def _index_of_data(self, value):
        # Show the single value common to the whole selection
        return self.findData(value)
