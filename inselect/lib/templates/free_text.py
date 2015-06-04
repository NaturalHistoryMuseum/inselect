# -*- coding: UTF-8 -*-
"""Generic template for microscope slides
"""

import re
from functools import partial

from inselect.lib.metadata import MetadataTemplate
from inselect.lib.parse import parse_matches_regex


_DIGITS = partial(parse_matches_regex, re.compile('^[0-9]+$'),
                  'Invalid value [{0}]: should contain only digits')

template = MetadataTemplate(
{
    'Name': 'Free text location and taxonomy',
    'Object label': u'{catalogNumber}_{Location-value}_{Taxonomy-value}',
    'Cropped file suffix': u'.jpg',
    'Fields': [
        {
            "Name": "catalogNumber",
            "Label": "Catalog number",
            "URI": "http://rs.tdwg.org/dwc/terms/catalogNumber",
            "Mandatory": True,
            "Parser": partial(parse_matches_regex, re.compile('^[0-9]{9}$'),
                        'Invalid value [{0}]: should contain nine digits'),
        },
        {
            "Name": "Location",
            "Mandatory": True,
            "Parser": _DIGITS,
        },
        {
            "Name": "Taxonomy",
            "Mandatory": True,
            "Parser": _DIGITS,
        },
    ]
})
