import re

from collections import OrderedDict

import yaml

from schematics.exceptions import ValidationError
from schematics.models import Model
from schematics.types import StringType, DecimalType, BooleanType, URLType
from schematics.types.compound import ListType, DictType, ModelType

from inselect.lib import parse
from inselect.lib.document import InselectDocument
from inselect.lib.ingest import IMAGE_SUFFIXES
from inselect.lib.utils import duplicated


# A dict {name: parse function}. Names are strings that the user
# can give as 'Parser' for a field.
# Remove the leading 'parse_' from the names.
PARSERS = {k: v for k, v in parse.PARSERS.iteritems()}
PARSERS = {re.sub(r'^parse_', '', k): v for k, v in PARSERS.iteritems()}

# Fields synthesized by UserTemplate.metadata()
RESERVED_FIELD_NAMES = ['ItemNumber']


# TODO Check for Field-value / 'Choices with data' collisions

class _UniqueListType(ListType):
    "A ListType that guarantees values are unique and non-empty."
    def validate_values_non_empty(self, value):
        if any(not v for v in value):
            raise ValidationError('Values must be non-empty.')

    def validate_unique(self, value):
        if duplicated(value):
            raise ValidationError('Values must be unique.')


class _FieldModel(Model):
    name = StringType(required=True, serialized_name='Name')
    label = StringType(serialized_name='Label')
    group = StringType(serialized_name='Group')
    uri = URLType(serialized_name='URI')
    mandatory = BooleanType(default=False, serialized_name='Mandatory')
    choices = _UniqueListType(StringType, serialized_name='Choices')
    choices_with_data = DictType(StringType,
        serialized_name='Choices with data')
    parser = StringType(choices=list(sorted(PARSERS.iterkeys())),
        serialized_name='Parser')
    regex_parser = StringType(serialized_name='Regex parser')

    def __repr__(self):
        return "_FieldModel ['{0}']".format(self.name)

    def __str__(self):
        return repr(self)

    def validate_name(self, data, value):
        if value in RESERVED_FIELD_NAMES:
            msg = u"'Name' should not be one of {0}."
            raise ValidationError(msg.format(RESERVED_FIELD_NAMES))

    def validate_choices(self, data, value):
        "'Choices' and 'Choices with data' are mutually exclusive"
        if data.get('choices') and data.get('choices_with_data'):
            msg = "'Choices' and 'Choices with data' are mutually exclusive."
            raise ValidationError(msg)

    def validate_parser(self, data, value):
        "'Parser' and 'Regex parser' are mutually exclusive"
        if data.get('parser') and data.get('regex_parser'):
            msg = "'Parser' and 'Regex parser' are mutually exclusive."
            raise ValidationError(msg)


def _validate_fields_not_empty(fields):
    "One or more fields must be defined."
    if not fields:
        raise ValidationError("One or more fields must be defined.")

def _validate_field_names_unique(fields):
    "Field names must be unique"
    if any(duplicated(f.name for f in fields)):
        raise ValidationError("Names must be unique")

def _validate_field_labels_unique(fields):
    "Field labels must be unique"
    if any(duplicated(f.label for f in fields)):
        raise ValidationError("Labels must be unique")


class _UserTemplateModel(Model):
    name = StringType(required=True, serialized_name='Name')
    object_label = StringType(serialized_name='Object label',
        default='{ItemNumber:04}')
    thumbnail_width_pixels = DecimalType(
        default=InselectDocument.THUMBNAIL_DEFAULT_WIDTH,
        min_value=InselectDocument.THUMBNAIL_MIN_WIDTH,
        max_value=InselectDocument.THUMBNAIL_MAX_WIDTH,
        serialized_name='Thumbnail width pixels')
    cropped_file_suffix = StringType(default='.jpg',
        choices=IMAGE_SUFFIXES, serialized_name='Cropped file suffix')
    fields = ListType(ModelType(_FieldModel),
        serialized_name='Fields',
        validators=[_validate_fields_not_empty,
                    _validate_field_names_unique,
                    _validate_field_labels_unique])

    def __repr__(self):
        return "_UserTemplateModel ['{0}']".format(self.name)

    def __str__(self):
        return repr(self)


def _ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    """Loads YAML mappings as OrderedDicts
    """
    # See http://stackoverflow.com/a/21912744/1773758
    class OrderedLoader(Loader):
        pass
 
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
 
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


def _extract_validation_error(e, prompt=None):
    """Given ValidationError e returns a list of strings of validation failures
    """
    # e.messages can be a list, tuple or dict
    msg = u'{0}: {1}'
    if isinstance(e.messages, dict):
        # Tedious work to unpick the possible formats
        messages = []
        for field, field_messages in e.messages.iteritems():
            if isinstance(field_messages, list):
                for field_message in field_messages:
                    messages.append(msg.format(field, field_message))
            else:
                messages.append(field, field_messages)
    else:
        message = e.messages

    if prompt:
        return [msg.format(prompt, m) for m in messages]
    else:
        return messages

def load_specification_from_file(path):
    "Load and returns the specification in the YAML document at path"
    return _ordered_load(path, yaml.SafeLoader)

def validated_specification(spec):
    "Returns a validated template specification"
    model = _UserTemplateModel({k: v for k, v in spec.iteritems() if 'Fields' != k})

    failures = []
    model.fields = []
    for f in spec.get('Fields', []):
        field = _FieldModel(f)
        try:
            field.validate()
        except ValidationError, e:
            failures += _extract_validation_error(e, prompt=f.get('Name'))
        model.fields.append(field)

    try:
        model.validate()
    except ValidationError, e:
        failures += _extract_validation_error(e)

    if failures:
        raise InvalidSpecificationError(failures)
    else:
        return model.to_native()


class InvalidSpecificationError(Exception):
    "Invalid user template specification"
    def __init__(self, problems):
        if 1 == len(problems):
            msg = '1 problem:\n{0}'.format(problems[0])
        else:
            msg = '{0} problems:\n{1}'
            msg = msg.format(len(problems), u'\n'.join(problems))
        super(InvalidSpecificationError, self).__init__(msg)
        self.problems = problems
