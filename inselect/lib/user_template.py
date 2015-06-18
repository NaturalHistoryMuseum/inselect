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

import yaml

from inselect.lib import parse

from inselect.lib.parse import parse_matches_regex
from inselect.lib.ingest import IMAGE_SUFFIXES_RE, IMAGE_SUFFIXES
from inselect.lib.utils import debug_print, duplicated, FormatDefault


# A dict {name: parse function}. Names are strings that the user
# can give as 'Parser' for a field.
# Remove the leading 'parse_' from the names.
PARSERS = {k: v for k, v in parse.PARSERS.iteritems()}
PARSERS = {re.sub(r'^parse_', '', k): v for k, v in PARSERS.iteritems()}


# TODO Split code

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
 
 
# Validation alternatives
#   http://rx.codesimply.com/
#   https://github.com/alecthomas/voluptuous
#   http://rx.codesimply.com/
 
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


def validate_specification(spec):
    """Validates that the dict conforms to the metadata template specification.
    Raises InvalidSpecificationError if any problems are found.
    """
    problems = []
    if not spec.get('Name'):
        problems.append('No template name')
    elif not isinstance(spec['Name'], basestring):
        problems.append('Template name should be a string')

    _validate_thumbnail_width(spec, problems)
    _validate_cropped_file_suffix(spec, problems)
    _validate_fields(spec, problems)

    if problems:
        raise InvalidSpecificationError(problems)

def _validate_thumbnail_width(spec, problems):
    if 'Thumbnail width pixels' in spec:
        # TODO Limits to come from inselect.lib.ingest
        MIN, MAX = 1024, 16384
        width = spec['Thumbnail width pixels']
        if not MIN <= width <= MAX:
            msg = (u'Invalid "Thumbnail width pixels" [{0}]. Must be between '
                   u'[{1}] and [{2}]')
            problems.append(msg.format(width, MIN, MAX))

def _validate_cropped_file_suffix(spec, problems):
    if 'Cropped file suffix' in spec:
        # Is a valid file suffix?
        suffix = spec['Cropped file suffix']
        if not IMAGE_SUFFIXES_RE.match(suffix):
            msg = u'Invalid "Cropped file suffix" [{0}]. Must be one of [{1}]'
            problems.append(msg.format(suffix, ', '.join(IMAGE_SUFFIXES)))

def _validate_fields(spec, problems):
    """Validates that the list of fields conforms to the metadata template
    specification
    """
    if not spec.get('Fields'):
        problems.append('No fields defined')
    else:
        fields = spec['Fields']
        if any(not f.get('Name') for f in fields):
            problems.append(u'One or more fields do not have a name')
        else:
            # The remaining checks require that field names are given
            _validate_field_names(fields, problems)
            _validate_field_labels(fields, problems)
            _validate_field_choices(fields, problems)
            _validate_field_choices_with_data(fields, problems)
            _validate_field_parsers(fields, problems)

def _validate_field_names(fields, problems):
    "Ensures that no names are duplicated"
    for dup in duplicated(f['Name'] for f in fields):
        msg = u'Duplicated field name [{0}]'
        problems.append(msg.format(dup))
 
    if any(f['Name'] in UserTemplate.RESERVED_FIELD_NAMES for f in fields):
        msg = u'Fields cannot be called {0}'
        problems.append(msg.format(list(UserTemplate.RESERVED_FIELD_NAMES)))

def _validate_field_labels(fields, problems):
    "Ensures that label, where given, are not empty and are unique"
    for empty in (f['Name'] for f in fields if 'Label' in f and not f['Label']):
        msg = u'Empty label for [{0}]'
        problems.append(msg.format(empty))

    # Label, if given, must be unique
    for dup in duplicated(f['Label'] for f in fields if 'Label' in f):
        msg = u'Duplicated label [{0}]'
        problems.append(msg.format(dup))

def _validate_field_choices(fields, problems):
    "Can't give both Choices and 'Choices with data'"
    for bad in ifilter(lambda f: 'Choices' in f and 'Choices with data' in f,
                       fields):
        msg = u'Both "Choices" and "Choices with data" given for [{0}]'
        problems.append(msg.format(bad['Name']))

    # Validate Choices
    for field in ifilter(lambda f: 'Choices' in f, fields):
        if not field['Choices']:
            # No choices
            msg = u'Empty "Choices" for [{0}]'
            problems.append(msg.format(field['Name']))
 
        for dup in duplicated(field['Choices']):
            # Labels in Choices must be unique
            msg = u'Duplicated "Choices" for [{0}]: [{1}]'
            problems.append(msg.format(field['Name'], dup))

def _validate_field_choices_with_data(fields, problems):
    "Validates 'Choices with data'"
    defined_field_names = set(f['Name'] for f in fields)
    for field in ifilter(lambda f: 'Choices with data' in f, fields):
        # A field named '{0}-value' will be synthesized for
        # ChoicesWithData fields - make sure that no fields have been
        # defined with this name
        value_field = '{0}-value'.format(field['Name'])
 
        if value_field in defined_field_names:
            msg = u'A field named "{0}" cannot be defined'
            problems.append(msg.format(value_field))
 
        if not field['Choices with data']:
            # No choices
            msg = u'Empty "Choices with data" for [{0}]'
            problems.append(msg.format(field['Name']))

def _validate_field_parsers(fields, problems):
    "Validates that 'Parser', where given, is in the list of parse functions"
    for bad in ifilter(lambda f: 'Parser' in f and f['Parser'] not in PARSERS, fields):
        msg = u'Unrecognised parser for [{0}]: [{1}]'
        problems.append(msg.format(bad['Name'], bad['Parser']))
 
    for bad in ifilter(lambda f: 'Parser' in f and 'Regex parser' in f, fields):
        msg = u'Both "Parser" and "Regex parser" given for [{0}]'
        problems.append(msg.format(bad['Name']))


_Field = namedtuple('_Field', ('name', 'label', 'group', 'mandatory', 'choices',
                               'choices_with_data', 'parse_fn'))

class UserTemplate(object):
    """A user-defined project template
    """

    EXTENSION = '.inselect_template'

    # Fields synthensized by the metadata() method
    RESERVED_FIELD_NAMES = ('ItemNumber',)

    def __init__(self, spec):
        validate_specification(spec)
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

    @classmethod
    def from_yaml(cls, doc):
        """Returns a new instance of UserTemplate constructed on doc
        """
        # usage example:
        return cls(_ordered_load(doc, yaml.SafeLoader))

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
        elif field in self.parse_mapping:
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
