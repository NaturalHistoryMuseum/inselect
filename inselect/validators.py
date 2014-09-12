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