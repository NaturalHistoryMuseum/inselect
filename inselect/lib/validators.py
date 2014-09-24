import string


class ValidationError(Exception):
    """Exception raised on validation error"""
    pass


def not_empty(value):
    """Validates the value as empty

    Parameters
    ----------
    value : str, list
        Value to validate

    Raises
    -------
    ValidationError
    """
    if len(value) == 0:
        raise ValidationError("{label} cannot be empty")
    return len(value) > 0


def is_annotation_field(value):
    """Ensures that the value is a field from the annotation fields

    Parameters
    ----------
    value : str

    Raises
    ------
    ValidationError
    """
    #TODO: Check if this works if the field has just been added.
    import inselect.settings
    fields = inselect.settings.get('annotation_fields')
    if value not in fields:
        raise ValidationError(
            ("{} is not one of the annotation fields.<br/>Note that these are "
             + "case sensitive").format(value)
        )


def validate_export_template(value):
    """Ensure that all placeholders exist as fields

    Parameters
    ----------
    value : str

    Raises
    ------
    ValidationError
    """
    placeholders = []
    try:
        for text, name, spec, conv in string.Formatter().parse(value):
            if name:
                placeholders.append(name)
    except ValueError:
        raise ValidationError("Curly brackets must either {{surround}} a value or be doubled (eg. {{{{)")
    #TODO: Check if this works if the field has just been added.
    import inselect.settings
    fields = inselect.settings.get('annotation_fields')
    unknown = set(placeholders) - set(fields)
    if len(unknown) > 0:
        raise ValidationError("Unknown placeholder(s): " + ", ".join(unknown) + ".<br/>Note that placeholders are case "
                                                                                "sensitive")