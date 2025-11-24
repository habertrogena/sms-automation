def is_valid_number(number: str) -> bool:
    """
    Very basic validation:
    - Must be digits only
    - At least 7 characters
    """
    return number.isdigit() and len(number) >= 7
