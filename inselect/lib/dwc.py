"""
"""
from __future__ import print_function

import dateutil.parser
import json
import re

from collections import OrderedDict
from itertools import chain, ifilter
from pathlib import Path

from .dwc_terms import DWC_TERMS
from .parse import (parse_latitude, parse_int, parse_float,
                    parse_int_gt0, parse_float_gt0,
                    parse_four_digit_int, parse_one_or_two_digit_int,
                    parse_latitude, parse_longitude,
                   )
from .utils import debug_print, duplicated, unique_everseen

# TODO Check against term types and date-time reg ex int
# http://rs.tdwg.org/dwc/tdwg_basetypes.xsd
validators = {'duplicated': dateutil.parser.parse,
              'individualCount': parse_int_gt0,
              'eventDate': dateutil.parser.parse,
              'eventTime': dateutil.parser.parse,
              'year': parse_four_digit_int,
              'month': parse_one_or_two_digit_int,
              'day': parse_one_or_two_digit_int,
              'minimumElevationInMeters': parse_float_gt0,
              'maximumElevationInMeters': parse_float_gt0,
              'minimumDepthInMeters': parse_float_gt0,
              'maximumDepthInMeters': parse_float_gt0,
              'minimumDistanceAboveSurfaceInMeters': parse_float_gt0,
              'maximumDistanceAboveSurfaceInMeters': parse_float_gt0,
              'decimalLatitude': parse_latitude,
              'parse_longitude': parse_longitude,
              'coordinateUncertaintyInMeters': parse_float_gt0,
              'coordinatePrecision': parse_float_gt0,
              'georeferencedDate': dateutil.parser.parse,
              'dateIdentified': dateutil.parser.parse,
              'namePublishedInYear': parse_four_digit_int,
              'measurementDeterminedDate': dateutil.parser.parse,
             }

class DWCTerms(object):
    """Darwin Core terms
    """

    def __init__(self, terms):
        """terms - a list of dicts
        """

        # Name field must be present
        if any('Name' not in t for t in terms):
            raise ValueError(u'One or more items do not have a name')

        # Shouldn't contain fields that we do not recognise
        fields = {'Group','Group label','Name','Label','URI','Type',
                  'Parser','Choices'}
        keys = set(chain(*(t.keys() for t in terms)))
        unrecognised = keys.difference(fields)
        if unrecognised:
            msg = u'Unrecognised keys {0}'
            raise ValueError(msg.format(sorted(list(unrecognised))))

        # No names should be duplicated
        names = [t['Name'] for t in terms]
        dup = duplicated(names)
        if dup:
            msg = u'Duplicated terms {0}'
            raise ValueError(msg.format(sorted(list(dup))))

        # Set parse functions
        for t in ifilter(lambda t: t['Name'] in validators, terms):
            t['Parser'] = validators[t['Name']]

        # Choices must be lists with no duplicates
        for term in ifilter(lambda t: 'Choices' in t, terms):
            if duplicated(term['Choices']):
                msg = u'Duplicated "Choices" for [{0}]'
                raise ValueError(msg.format(term['Name']))
            elif not term['Choices']:
                msg = u'Empty "Choices" for [{0}]'
                raise ValueError(msg.format(term['Name']))

        self.terms = terms

        # Ordered mapping from group name to label
        groups = [(t['Group'], t['Group label']) for t in terms]
        self.groups = OrderedDict(unique_everseen(groups))

    @classmethod
    def from_json(cls, path):
        "Loads JSON data in path and returns new DWCTerms instance"
        return cls(json.load(Path(path).open()))


DWC_TERMS = DWCTerms(DWC_TERMS).terms


if '__main__' == __name__:
    import sys
    terms = DWCTerms.from_json(sys.argv[1]).terms
    m = u'{0:40} {1:40} {2:30} {3:3}'
    print(m.format('Group', 'Name', 'Parser', 'Choices'))
    for t in terms:
        print(m.format(t['Group'], t['Name'],
                       t['Parser'].__name__ if 'Parser' in t else '',
                       len(t.get('Choices', []))))
