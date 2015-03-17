"""Template for Diana Percy's microscope slides project
"""

import re
from functools import partial

from inselect.lib.metadata import MetadataTemplate
from inselect.lib.parse import parse_matches_re, parse_int_gt0


template = MetadataTemplate(
{
    'Name': 'Percy slides',
    'Object label': u'{catalogNumber}-{family}',
    'Fields': [
        {
          "Name": "catalogNumber",
          "Label": "Catalog number",
          "URI": "http://rs.tdwg.org/dwc/terms/catalogNumber",
          "Mandatory": True,
          "Parser": partial(parse_matches_re, re.compile('^[0-9]{5,10}$'),
                'Invalid value [{0}]: must be between 5 and 10 digits'),
        },
        {
            "Name": "Location",
            "Mandatory": True,
            "ChoicesWithLabels" : {
                123: 'Drawer 8',
                124: 'Drawer 9',
                125: 'Drawer 10',
                126: 'Drawer 11',
            },
            "Default": 125,
        },
        {
            "Name": "individualCount",
            "Label": "Individual count",
            "URI": "http://rs.tdwg.org/dwc/terms/individualCount",
            "Default": 1,
            "Parser": parse_int_gt0,
        },
        {
            "Name": "A user-defined field",
        },
        {
            "Name": "scientificName",
            "Label": "Scientific name",
            "URI": "http://rs.tdwg.org/dwc/terms/scientificName",
        },
        {
            "Name": "kingdom",
            "Label": "Kingdom",
            "URI": "http://rs.tdwg.org/dwc/terms/kingdom",
        },
        {
            "Name": "phylum",
            "Label": "Phylum",
            "URI": "http://rs.tdwg.org/dwc/terms/phylum",
        },
        {
            "Name": "class",
            "Label": "Class",
            "URI": "http://rs.tdwg.org/dwc/terms/class",
        },
        {
            "Name": "order",
            "Label": "Order",
            "URI": "http://rs.tdwg.org/dwc/terms/order",
        },
        {
            "Name": "family",
            "Label": "Family",
            "URI": "http://rs.tdwg.org/dwc/terms/family",
        },
        {
            "Name": "genus",
            "Label": "Genus",
            "URI": "http://rs.tdwg.org/dwc/terms/genus",
        },
        {
            "Name": "specificEpithet",
            "Label": "Specific epithet",
            "URI": "http://rs.tdwg.org/dwc/terms/specificEpithet",
        },
        {
            "Name": "taxonRank",
            "Label": "Taxon rank",
            "URI": "http://rs.tdwg.org/dwc/terms/taxonRank",
        },
        {
            "Name": "scientificNameAuthorship",
            "Label": "Scientific name authorship",
            "URI": "http://rs.tdwg.org/dwc/terms/scientificNameAuthorship",
        },
    ]
})
