from collections import Counter, namedtuple
from itertools import chain, count, izip


def validate_document(document, template):
    """Validates an InselectDocument against a UserTemplate and returns an
    instance of ValidationProblems
    """
    visitor = CollectProblemsVisitor()
    _validate_document(document, template, visitor)
    return visitor.all_problems()


def _validate_document(document, template, visitor):
    "Validates an InselectDocument against a UserTemplate"
    _visit_boxes(document, template, visitor)
    _visit_labels(document, template, visitor)


def _visit_boxes(document, template, visitor):
    for index, box in enumerate(document.items):
        _visit_box(template, visitor, index, box)


def _visit_box(template, visitor, index, box):
    box_label = template.format_label(1 + index, box['fields'])
    md = box['fields']
    for field in (f for f in template.mandatory if not md.get(f)):
        visitor.missing_mandatory(index, box_label, field)

    for field, parse in ((k, v) for k, v in template.parse_mapping.iteritems() if k in md):
        try:
            parse(md[field])
        except ValueError:
            visitor.failed_parse(index, box_label, field, md[field])


def _visit_labels(document, template, visitor):
    labels = [
        template.format_label(1 + index, box['fields'])
        for index, box in enumerate(document.items)
    ]

    # Labels must be given
    for index in (i for i, l in izip(count(), labels) if not l):
        visitor.missing_label(index)

    # Non-missing object labels must be unique
    counts = Counter(labels)
    for label in (v for v, n in counts.iteritems() if v and n > 1):
        visitor.duplicated_labels(label)

MissingMandatory = namedtuple('MissingMandatory', ['index', 'label', 'field'])
FailedParse = namedtuple('FailedParse', ['index', 'label', 'field', 'value'])


class CollectProblemsVisitor(object):
    """Collects validation problems
    """
    def __init__(self):
        self._missing_mandatory = []
        self._failed_parse = []
        self._missing_label = []
        self._duplicated_labels = []

    def missing_mandatory(self, index, label, field):
        self._missing_mandatory.append(MissingMandatory(index, label, field))

    def failed_parse(self, index, label, field, value):
        self._failed_parse.append(FailedParse(index, label, field, value))

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


def format_missing_mandatory(missing_mandatory):
    msg = u'Box [{0}] [{1}] lacks mandatory field [{2}]'
    for index, label, field in missing_mandatory:
        yield msg.format(1 + index, label, field)


def format_failed_parse(failed_parse):
    msg = u'Could not parse value of [{0}] [{1}] for box [{2}] [{3}]'
    for index, label, field, value in failed_parse:
        yield msg.format(field, value, 1 + index, label)


def format_missing_label(missing_label):
    msg = u'Missing object label for box [{0}]'
    for index in missing_label:
        yield msg.format(1 + index)


def format_duplicated_labels(duplicated_labels):
    msg = u'Duplicated object label [{0}]'
    for duplicated in duplicated_labels:
        yield msg.format(duplicated)


def format_validation_problems(v):
    "Generator function of validation failure messages for ValidationProblems v"
    return chain(format_missing_mandatory(v.missing_mandatory),
                 format_failed_parse(v.failed_parse),
                 format_missing_label(v.missing_label),
                 format_duplicated_labels(v.duplicated_labels))
