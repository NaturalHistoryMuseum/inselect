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


# Returns a dict {name: parse function}. Names are strings that the user
# can give as 'Parser' for a field. Remove the leading 'parse_' from the names
# and include only those functions that take a single argument called 'value'.
_PARSERS = {k: v for k, v in parse.PARSERS.iteritems()}
_PARSERS = {k: v for k, v in _PARSERS.iteritems() if ['value'] == inspect.getargspec(v).args}
_PARSERS = {re.sub(r'^parse_', '', k): v for k, v in _PARSERS.iteritems()}


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
    for bad in ifilter(lambda f: 'Parser' in f and f['Parser'] not in _PARSERS, fields):
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
        self._name = spec['Name']
        self._description = spec.get('Description', '')
        self._cropped_file_suffix = spec.get('Cropped file suffix', '.jpg')
        self._thumbnail_width_pixels = spec.get('Thumbnail width pixels', 4096)

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
                parse_fn = _PARSERS[field['Parser']]
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

        self._fields = fields

        # Map from field name to a instance of _Field
        self._fields_mapping = {f.name : f for f in fields}

        # Map from field name to field
        self._choices_with_data_mapping = {f.name : f for f in fields if f.choices_with_data}

        # Mapping from name to parse function, for those fields that have a parser
        self._parse_mapping = {f.name : f.parse_fn for f in fields if f.parse_fn}

        # List of mandatory fields
        self._mandatory = [f.name for f in fields if f.mandatory]
 
    @classmethod
    def from_yaml(cls, doc):
        """Returns a new instance of UserTemplate constructed on doc
        """
        # usage example:
        return cls(_ordered_load(doc, yaml.SafeLoader))
 
    def __repr__(self):
        msg = '<UserTemplate [{0}] with {1} fields>'
        return msg.format(self._name, len(self._fields))
 
    def __str__(self):
        msg = 'UserTemplate [{0}] with {1} fields'
        return msg.format(self._name, len(self._fields))
 
    @property
    def name(self):
        "The template's name"
        return self._name
 
    @property
    def fields(self):
        "A list of instances of _Field"
        return self._fields
 
    def field_names(self):
        "Generator function of field names and names of synthesized fields"
        for name in self.RESERVED_FIELD_NAMES:
            yield name
 
        for field in self._fields:
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
        for field in self._choices_with_data_mapping.itervalues():
            value = field.choices_with_data.get(md.get(field.name), '')
            md[u'{0}-value'.format(field.name)] = value
        return md
 
    def format_label(self, index, metadata):
         "Returns a textual label for the given box index and metadata"
         return self._format_label(**self.metadata(index, metadata))
 
    @property
    def cropped_file_suffix(self):
        "The suffix to use for cropped image files"
        return self._cropped_file_suffix
 
    @property
    def thumbnail_width_pixels(self):
        "The width of the thumbnail image, in pixels"
        return self._thumbnail_width_pixels
 
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
            if any(not metadata.get(f) for f in self._mandatory):
                return False
            try:
                parseable = self._parse_mapping.iteritems()
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
        if field not in self._fields_mapping:
            # A field that this template does not know about
            return True
        elif not value and field in self._mandatory:
            # Field is mandatory and no value was provided
            return False
        elif field in self._parse_mapping:
            parse = self._parse_mapping[field]
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
 
    def visit_document(self, document, visitor):
        """
        """
        visitor.begin_visit(document)
        self._visit_boxes(document, visitor)
        self._visit_labels(document, visitor)
        visitor.end_visit(document)
 
    def _visit_boxes(self, document, visitor):
        for index, box in enumerate(document.items):
            self._visit_box(visitor, index, box)
 
    def _visit_box(self, visitor, index, box):
        box_label = self.format_label(1+index, box['fields'])
        md = box['fields']
        for field in (f for f in self._mandatory if not md.get(f)):
            visitor.missing_mandatory(index, box_label, field)
 
        for field, parse in ( (k, v) for k, v in self._parse_mapping.iteritems() if k in set(md.keys())):
            try:
                parse(md[field])
            except ValueError:
                visitor.failed_parse(index, box_label, field)
 
    def _visit_labels(self, document, visitor):
        """Visit the document
        """
        labels = [self.format_label(1+index, box['fields']) for index, box in enumerate(document.items)]
 
        # Labels must be given
        for index in (i for i, l in izip(count(), labels) if not l):
            visitor.missing_label(index)
 
        # Non-missing object labels must be unique
        counts = Counter(labels)
        for label in (v for v, n in counts.iteritems() if v and n > 1):
            visitor.duplicated_labels(label)
 
 
class MetadataVisitor(object):
    def begin_visit(self, document):
        pass
 
    def missing_mandatory(self, index, label, field):
        pass
 
    def failed_parse(self, index, label, field):
        pass
 
    def missing_label(self, index):
        pass
 
    def duplicated_labels(self, label):
        pass
 
    def end_visit(self, document):
        pass
 
 
class PrintVisitor(MetadataVisitor):
    def begin_visit(self, document):
        print('begin_visit', document)
 
    def missing_mandatory(self, index, label, field):
        print('missing_mandatory', box, field)
 
    def failed_parse(self, index, label, field):
        print('failed_parse', box, field)
 
    def missing_label(self, index):
        print('missing_label', index)
 
    def duplicated_labels(self, label):
        print('duplicated_labels', label)
 
    def end_visit(self, document):
        print('end_visit', document)
 
 
MissingMandatory = namedtuple('MissingMandatory', ['index', 'label', 'field'])
FailedParse = namedtuple('FailedParse', ['index', 'label', 'field'])
 
class CollectVisitor(MetadataVisitor):
    """Collects validation problems
    """
    def begin_visit(self, document):
        self._missing_mandatory = []
        self._failed_parse = []
        self._missing_label = []
        self._duplicated_labels = []
 
    def missing_mandatory(self, index, label, field):
        self._missing_mandatory.append(MissingMandatory(index, label, field))
 
    def failed_parse(self, index, label, field):
        self._failed_parse.append(FailedParse(field, index, label))
 
    def missing_label(self, index):
        self._missing_label.append(index)
 
    def duplicated_labels(self, label):
        self._duplicated_labels.append(label)
 
    def all_problems(self):
        return ValidationProblems(self._missing_mandatory, self._failed_parse,
                                  self._missing_label, self._duplicated_labels)
 
 
class ValidationProblems(object):
    """A container of validation problems
    """
    def __init__(self, missing_mandatory, failed_parse, missing_label,
                 duplicated_labels):
        self.missing_mandatory = missing_mandatory
        self.failed_parse = failed_parse
        self.missing_label = missing_label
        self.duplicated_labels = duplicated_labels
 
    @property
    def any_problems(self):
        return bool(self.missing_mandatory or
                    self.failed_parse or
                    self.missing_label or
                    self.duplicated_labels)
 
 
if '__main__' == __name__:
    print('Values that can be used in the "Parse" section of a field '
          'specification')
    for n in sorted(_PARSERS.keys()):
        print(n)
        print(_PARSERS[n].__doc__)
