"""Metadata field template
"""
from __future__ import print_function

import json
import re

from collections import OrderedDict
from functools import partial
from itertools import chain, ifilter
from pathlib import Path

from inselect.lib.utils import (debug_print, duplicated, unique_everseen,
                                FormatDefault)


class MetadataTemplate(object):
    """Metadata fields template
    """

    def __init__(self, template):
        """template - a list that conforms for the metatadata template spec
        """

        if not template.get('Name'):
            raise ValueError('No name')

        fields = template['Fields']

        # Name field must be present
        if any('Name' not in f for f in fields):
            raise ValueError(u'One or more items do not have a name')

        # No names should be duplicated
        names = [f['Name'] for f in fields]
        dup = duplicated(names)
        if dup:
            msg = u'Duplicated fields {0}'
            raise ValueError(msg.format(sorted(list(dup))))

        # Reserved name
        if 'ItemNumber' in names:
            raise ValueError("'ItemNumber' is a reserved field name")

        # Choices must be lists with no duplicates
        # TODO Validate choices values vs labels and vs default
        for field in ifilter(lambda t: 'Choices' in t, fields):
            if duplicated(field['Choices']):
                msg = u'Duplicated "Choices" for [{0}]'
                raise ValueError(msg.format(field['Name']))
            elif not field['Choices']:
                msg = u'Empty "Choices" for [{0}]'
                raise ValueError(msg.format(field['Name']))

        self._name = template['Name'].strip()
        self._fields = fields

        # A method that returns labels from metadata dicts
        self.format_label = partial(FormatDefault(default='').format,
                                    template.get('Object label', ''))
        self.format_label.__doc__ = "Returns a string assembled from metadata values"

        # Map fromm field name to field
        self._fields_mapping = {f['Name'] : f for f in fields}

        # Mapping from name to field for fields that have a parser
        self._parse_mapping = {k: v for k, v in self._fields_mapping.iteritems() if 'Parser' in v}

        # List of mandatory fields
        self._mandatory = [f['Name'] for f in self._fields if f.get('Mandatory')]

    def __repr__(self):
        msg = '<MetadataTemplate [{0}] with {1} fields>'
        return msg.format(self._name, len(self._fields))

    def __str__(self):
        msg = 'MetadataTemplate [{0}] with {1} fields'
        return msg.format(self._name, len(self._fields))

    @property
    def name(self):
        """The template's name
        """
        return self._name

    @property
    def fields(self):
        """List of fields
        """
        return self._fields

    @property
    def mandatory(self):
        """List of names of mandatory fields
        """
        return self._mandatory

    def validate_record(self, record):
        """Returns True if record validates against this template; False if not
        """
        # Mandatory fields
        if any(not record.get(f) for f in self.mandatory):
            return False

        try:
            for k in set(self._parse_mapping.keys()).intersection(record.keys()):
                self._parse_mapping[k]['Parser'](record[k])
        except ValueError:
            return False
        else:
            return True

    def validate_field(self, field, value):
        """Returns True if field value validates against this template; False if
        not
        """
        if field not in self._fields_mapping:
            # A field that this template does not know about
            return True
        elif not value and field in self.mandatory:
            # Field is mandatory and no value was provided
            return False
        elif value:
            # Attempt to parse the value
            parse = self._fields_mapping[field].get('Parser')
            if parse:
                try:
                    debug_print('Parse [{0}] [{1}]'.format(field, value))
                    parse(value)
                except ValueError:
                    # Could not be parsed
                    debug_print('Failed parse [{0}] [{1}]'.format(field, value))
                    return False

        # The value is valid
        return True
