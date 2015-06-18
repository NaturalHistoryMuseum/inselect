"""User-defined templates
"""
from __future__ import print_function
 
import inspect
import json
import re
import sys

from collections import Counter, namedtuple, OrderedDict
from functools import partial
from itertools import count, ifilter, izip

from inselect.lib import parse

from inselect.lib.parse import parse_matches_regex
from inselect.lib.ingest import IMAGE_SUFFIXES_RE, IMAGE_SUFFIXES
from inselect.lib.utils import debug_print, FormatDefault


# A dict {name: parse function}. Names are strings that the user
# can give as 'Parser' for a field.
# Remove the leading 'parse_' from the names.
PARSERS = {k: v for k, v in parse.PARSERS.iteritems()}
PARSERS = {re.sub(r'^parse_', '', k): v for k, v in PARSERS.iteritems()}


_Field = namedtuple('_Field', ('name', 'label', 'group', 'uri', 'mandatory',
                               'choices', 'choices_with_data', 'parse_fn'))

class UserTemplate(object):
    """A user-defined project template
    """

    EXTENSION = '.inselect_template'

    # Fields synthensized by the metadata() method
    RESERVED_FIELD_NAMES = ['ItemNumber']

    def __init__(self, spec):
        self.name = spec['Name']
        self.description = spec.get('Description', '')
        self.cropped_file_suffix = spec.get('Cropped file suffix', '.jpg')
        self.thumbnail_width_pixels = spec.get('Thumbnail width pixels', 4096)

        # A method that returns labels from metadata dicts
        self._format_label = partial(FormatDefault(default='').format,
                                     spec.get('Object label', '{ItemNumber:04}'))

        # A list of instance of _Field
        fields = []
        for field in spec['Fields']:
            choices_with_data = None
            if 'Choices with data' in field:
                choices_with_data = OrderedDict(field['Choices with data'])

            parse_fn = None
            if 'Parser' in field:
                parse_fn = PARSERS[field['Parser']]
            elif 'Regex parser' in field:
                regex = field['Regex parser']
                parse_fn = partial(parse_matches_regex, re.compile(regex))

            fields.append(_Field(name=field['Name'],
                                 label=field.get('Label', field['Name']),
                                 group=field.get('Group'),
                                 uri=field.get('URI'),
                                 mandatory=field.get('Mandatory', False),
                                 choices=field.get('Choices'),
                                 choices_with_data=choices_with_data,
                                 parse_fn=parse_fn))

        self.fields = fields

        # Map from field name to a instance of _Field
        self.fields_mapping = {f.name : f for f in fields}

        # Map from field name to field
        self.choices_with_data_mapping = {f.name : f for f in fields if f.choices_with_data}

        # Mapping from name to parse function, for those fields that have a parser
        self.parse_mapping = {f.name : f.parse_fn for f in fields if f.parse_fn}

        # Set of mandatory fields
        self.mandatory = set(f.name for f in fields if f.mandatory)

    def __repr__(self):
        msg = '<UserTemplate [{0}] with {1} fields>'
        return msg.format(self.name, len(self.fields))

    def __str__(self):
        msg = 'UserTemplate [{0}] with {1} fields'
        return msg.format(self.name, len(self.fields))

    def field_names(self):
        "Generator function of field names and names of synthesized fields"
        for name in self.RESERVED_FIELD_NAMES:
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
        if False:
            # DRY
            for field, value in metadata.iteritems():
                if not self.validate_field(field, value):
                    return False
            return True
        else:
            # Performs better?
            if any(not metadata.get(f) for f in self.mandatory):
                return False
            try:
                parseable = self.parse_mapping.iteritems()
                parseable = ((k, v) for k, v in parseable if k in metadata)
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
                debug_print('Parsed [{0}] [{1}]'.format(field, value))
                return True
            except ValueError:
                # Could not be parsed
                debug_print('Failed to parse [{0}] [{1}]'.format(field, value))
                return False
        else:
            return True
 

if '__main__' == __name__:
    print('Values that can be used in the "Parse" section of a field '
          'specification')
    for n in sorted(PARSERS.keys()):
        print(n)
        print(PARSERS[n].__doc__)
