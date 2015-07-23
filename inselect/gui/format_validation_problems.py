"""Functions for formatting metadata validation problems
"""

# These functions in gui rather than lib to allow for translations using Qt's
# tr()

from itertools import chain

def format_missing_mandatory(missing_mandatory):
    msg = u'Box [{0}] [{1}] lacks mandatory field [{2}]'
    for index, label, field in missing_mandatory:
        yield msg.format(1 + index, label, field)

def format_failed_parse(failed_parse):
    msg = u'Could not parse value of [{0}] for box [{1}] [{2}]'
    for index, label, field in failed_parse:
        yield msg.format(1 + index, label, field)

def format_missing_label(missing_label):
    msg = u'Missing object label for box [{0}]'
    for index in missing_label:
        yield msg.format(1 + index)

def format_duplicated_labels(duplicated_labels):
    msg = u'Duplicated object label [{0}]'
    for duplicated in duplicated_labels:
        yield msg.format(duplicated)

def format_validation_problems(v):
    return chain(format_missing_mandatory(v.missing_mandatory),
                 format_failed_parse(v.failed_parse),
                 format_missing_label(v.missing_label),
                 format_duplicated_labels(v.duplicated_labels))
