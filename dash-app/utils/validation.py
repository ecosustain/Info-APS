
def is_valid(value):
    """Checks if a value is not None and not an empty list"""
    return not (value is None or (isinstance(value, list) and len(value) == 0))
