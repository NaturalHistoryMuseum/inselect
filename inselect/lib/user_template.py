"""User-defined templates
"""
import re

from collections import namedtuple, OrderedDict
from functools import partial
from pathlib import Path

import persist_user_template
from inselect.lib.parse import parse_matches_regex
from inselect.lib.utils import debug_print, FormatDefault


_Field = namedtuple('_Field', ('name', 'label', 'group', 'uri', 'mandatory',
                               'choices', 'choices_with_data', 'parse_fn'))


class UserTemplate(object):
    """A user-defined project template

    Clients should probaby create instances using one of the classmethods
    from_file or from_specification.
    """

    EXTENSION = '.inselect_template'

    def __init__(self, spec):
        self.name = spec['Name']
        self.cropped_file_suffix = spec['Cropped file suffix']
        self.thumbnail_width_pixels = spec['Thumbnail width pixels']

        # A method that returns labels from metadata dicts
        self._format_label = partial(FormatDefault(default='').format,
                                     spec['Object label'])

        # A list of instance of _Field
        fields = []
        for field in spec['Fields']:
            choices_with_data = None
            if field.get('Choices with data'):
                choices_with_data = OrderedDict(field['Choices with data'])

            # A parse function - either one of the parsers in defined in
            # persist_user_template.PARSERS, a regular expression or None
            parse_fn = None
            if field.get('Parser'):
                parse_fn = persist_user_template.PARSERS[field['Parser']]
            elif field.get('Regex parser'):
                regex = field['Regex parser']
                parse_fn = partial(parse_matches_regex, re.compile(regex))

            # Display label defaults to the field name
            label = field.get('Label')
            label = label if label else field['Name']
            fields.append(_Field(name=field['Name'],
                                 label=label,
                                 group=field.get('Group'),
                                 uri=field.get('URI'),
                                 mandatory=field.get('Mandatory', False),
                                 choices=field.get('Choices'),
                                 choices_with_data=choices_with_data,
                                 parse_fn=parse_fn))

        self.fields = fields

        # Map from field name to a instance of _Field
        self.fields_mapping = {f.name: f for f in fields}

        # Map from field name to field
        self.choices_with_data_mapping = {f.name: f for f in fields if f.choices_with_data}

        # Mapping from name to parse function, for those fields that have a parser
        self.parse_mapping = {f.name: f.parse_fn for f in fields if f.parse_fn}

        # Set of mandatory fields
        self.mandatory = set(f.name for f in fields if f.mandatory)

    def __repr__(self):
        msg = '<UserTemplate [{0}] with {1} fields>'
        return msg.format(self.name, len(self.fields))

    def __str__(self):
        msg = 'UserTemplate [{0}] with {1} fields'
        return msg.format(self.name, len(self.fields))

    @classmethod
    def load(cls, path):
        """Returns a new instance of UserTemplate using the YAML document at path
        """
        with Path(path).open(encoding='utf8') as infile:
            return cls.from_file(infile)

    @classmethod
    def from_file(cls, stream):
        """Returns a new instance of UserTemplate using the YAML document in
        stream
        """
        spec = persist_user_template.load_specification_from_file(stream)
        return cls.from_specification(spec)

    @classmethod
    def from_specification(cls, spec):
        "Returns a new instance of UserTemplate from spec"
        return cls(persist_user_template.validated_specification(spec))

    def field_names(self):
        "Generator function of field names and names of synthesized fields"
        for name in persist_user_template.RESERVED_FIELD_NAMES:
            yield name

        for field in self.fields:
            yield field.name
            if field.choices_with_data:
                yield u'{0}-value'.format(field.name)

    def metadata(self, index, metadata):
        """Returns a dict {field_name: value} for the given box index and
        metadata, adding synthesized values where required
        """
        # TODO Deep copy here?
        md = metadata
        md['ItemNumber'] = index

        # Consider fields with a 'Choices with data'
        for field in self.choices_with_data_mapping.itervalues():
            value = field.choices_with_data.get(md.get(field.name), '')
            md[u'{0}-value'.format(field.name)] = value
        return md

    def format_label(self, index, metadata):
        "Returns a textual label for the given box index and metadata"
        return self._format_label(**self.metadata(index, metadata))

    def validate_metadata(self, metadata):
        """Returns True if the dict metadata validates against this template;
        False if not
        """
        if any(not metadata.get(f) for f in self.mandatory):
            return False
        try:
            parseable = self.parse_mapping.iteritems()
            parseable = ((k, v) for k, v in parseable if metadata.get(k))
            for field, parse_fn in parseable:
                parse_fn(metadata[field])
        except ValueError:
            return False
        else:
            return True

    def validate_field(self, field, value):
        """Returns True if field/value validates against this template; False if
        not
        """
        if field not in self.fields_mapping:
            # A field that this template does not know about
            return True
        elif not value and field in self.mandatory:
            # Field is mandatory and no value was provided
            return False
        elif value and field in self.parse_mapping:
            parse = self.parse_mapping[field]
            try:
                parse(value)
                debug_print(u'Parsed [{0}] [{1}]'.format(field, value))
                return True
            except ValueError:
                # Could not be parsed
                debug_print(u'Failed to parse [{0}] [{1}]'.format(field, value))
                return False
        else:
            return True
