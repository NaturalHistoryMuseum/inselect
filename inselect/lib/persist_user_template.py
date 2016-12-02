import re

from collections import OrderedDict

import yaml

from schematics.exceptions import ModelConversionError, ValidationError
from schematics.models import Model
from schematics.types import StringType, DecimalType, BooleanType, URLType
from schematics.types.compound import (ListType, ModelType, MultiType, BaseType)

from inselect.lib import parse
from inselect.lib.document import InselectDocument
from inselect.lib.ingest import IMAGE_SUFFIXES
from inselect.lib.utils import duplicated


# A dict {name: parse function}. Names are strings that the user
# can give as 'Parser' for a field.
# Remove the leading 'parse_' from the names.
PARSERS = {k: v for k, v in parse.PARSERS.items()}
PARSERS = {re.sub(r'^parse_', '', k): v for k, v in PARSERS.items()}

# Fields relating to bounding box locations
BOUNDING_BOX_FIELD_NAMES = (
    'NormalisedLeft', 'NormalisedTop', 'NormalisedRight', 'NormalisedBottom',
    'ThumbnailLeft', 'ThumbnailTop', 'ThumbnailRight', 'ThumbnailBottom',
    'OriginalLeft', 'OriginalTop', 'OriginalRight', 'OriginalBottom',
)

# Fields synthesized by UserTemplate.metadata()
# TODO Cropped_image_name should be CroppedImageName for consistency with other
# field names
RESERVED_FIELD_NAMES = ('Cropped_image_name', 'ItemNumber') + BOUNDING_BOX_FIELD_NAMES


# TODO Check for Field-value / 'Choices with data' collisions

class _UniqueListType(ListType):
    "A ListType that guarantees values are unique and non-empty."
    def validate_values_non_empty(self, value):
        if any(not v for v in value):
            raise ValidationError('Values must be non-empty.')

    def validate_unique(self, value):
        if next(duplicated(value), None):
            raise ValidationError('Values must be unique.')


class OrderedDictType(MultiType):
    "Field that holds an OrderedDict. Copied from schematics/types/compound.py"
    def __init__(self, field, coerce_key=None, **kwargs):
        if not isinstance(field, BaseType):
            compound_field = kwargs.pop('compound_field', None)
            field = self.init_compound_field(field, compound_field, **kwargs)

        self.coerce_key = coerce_key or str
        self.field = field

        validators = [self.validate_items] + kwargs.pop("validators", [])

        super(OrderedDictType, self).__init__(validators=validators, **kwargs)

    @property
    def model_class(self):
        return self.field.model_class

    def to_native(self, value, safe=False, context=None):
        if value and isinstance(value, list) and 2 == len(value[0]):
            # Expect a list of tuples
            value = OrderedDict(value)
        if not isinstance(value, OrderedDict):
            raise ValidationError('Must be a mapping.')
        else:
            return OrderedDict(
                (self.coerce_key(k), self.field.to_native(v, context))
                for k, v in value.items()
            )

    def validate_items(self, items):
        errors = {}
        for key, value in items.items():
            try:
                self.field.validate(value)
            except ValidationError as exc:
                errors[key] = exc

        if errors:
            raise ValidationError(errors)

    def export_loop(self, dict_instance, field_converter,
                    role=None, print_none=False):
        """Loops over each item in the model and applies either the field
        transform or the multitype transform.  Essentially functions the same
        as `transforms.export_loop`.
        """
        data = OrderedDict()

        for key, value in dict_instance.items():
            if hasattr(self.field, 'export_loop'):
                shaped = self.field.export_loop(value, field_converter,
                                                role=role)
                feels_empty = shaped and len(shaped) == 0
            else:
                shaped = field_converter(self.field, value)
                feels_empty = shaped is None

            if feels_empty and self.field.allow_none():
                data[key] = shaped
            elif shaped is not None:
                data[key] = shaped
            elif print_none:
                data[key] = shaped

        if len(data) > 0:
            return data
        elif len(data) == 0 and self.allow_none():
            return data
        elif print_none:
            return data


class _FieldModel(Model):
    name = StringType(required=True, serialized_name='Name')
    label = StringType(serialized_name='Label')
    group = StringType(serialized_name='Group')
    uri = URLType(serialized_name='URI')
    fixed_value = StringType(serialized_name='Fixed value')
    mandatory = BooleanType(default=False, serialized_name='Mandatory')
    choices = _UniqueListType(StringType, serialized_name='Choices')
    choices_with_data = OrderedDictType(
        StringType,
        serialized_name='Choices with data'
    )
    parser = StringType(
        choices=list(sorted(PARSERS.keys())),
        serialized_name='Parser'
    )
    regex_parser = StringType(serialized_name='Regex parser')

    def __repr__(self):
        return "_FieldModel ['{0}']".format(self.name)

    def __str__(self):
        return repr(self)

    def validate_name(self, data, value):
        if value in RESERVED_FIELD_NAMES:
            msg = "Should not be one of {0}."
            raise ValidationError(msg.format(RESERVED_FIELD_NAMES))

    def validate_fixed_value(self, data, value):
        pass

    def validate_choices(self, data, value):
        "'Choices', 'Choices with data' and 'Fixed value' are mutually exclusive"
        if 1 < sum(bool(data.get(field)) for field in
                   ('choices', 'choices_with_data', 'fixed_value')):
            msg = ("'Choices', 'Choices with data' and 'Fixed value' are "
                   "mutually exclusive.")
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
    if next(duplicated(f.name for f in fields), None):
        raise ValidationError("Names must be unique")


def _validate_field_labels_unique(fields):
    "Field labels must be unique"
    if next(duplicated(f.label for f in fields), None):
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
                                     choices=IMAGE_SUFFIXES,
                                     serialized_name='Cropped file suffix')
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
    msg = '{0}: {1}'
    if isinstance(e.messages, dict):
        # Tedious work to unpick the possible formats
        messages = []
        for field, field_messages in e.messages.items():
            if isinstance(field_messages, list):
                for field_message in field_messages:
                    messages.append(msg.format(field, field_message))
            else:
                messages.append(msg.format(field, field_messages))
    else:
        messages = e.messages

    if prompt:
        return [msg.format(prompt, m) for m in messages]
    else:
        return messages


def load_specification_from_file(path):
    "Load and returns the specification in the YAML document at path"
    return _ordered_load(path, yaml.SafeLoader)


def validated_specification(spec):
    "Returns a validated template specification"
    model = _UserTemplateModel({k: v for k, v in spec.items() if 'Fields' != k})

    failures = []
    model.fields = []
    for f in spec.get('Fields', []):
        try:
            field = _FieldModel(f)
            field.validate()
        except (ModelConversionError, ValidationError) as e:
            failures += _extract_validation_error(e, prompt=f.get('Name'))
        else:
            model.fields.append(field)

    try:
        model.validate()
    except (ModelConversionError, ValidationError) as e:
        failures += _extract_validation_error(e)

    if failures:
        # TODO Order of error messages varies randomly. The order is dependent
        # upon (I think) object identities within schematics.
        raise InvalidSpecificationError(sorted(failures))
    else:
        return model.to_native()


class InvalidSpecificationError(Exception):
    "Invalid user template specification"
    def __init__(self, problems):
        if 1 == len(problems):
            msg = '1 problem:\n{0}'.format(problems[0])
        else:
            msg = '{0} problems:\n{1}'
            msg = msg.format(len(problems), '\n'.join(problems))
        super(InvalidSpecificationError, self).__init__(msg)
        self.problems = problems
