from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re


def is_valid_email(_string):
    try:
        validate_email(_string)
        return True
    except ValidationError:
        return False


# strings like 'New York, NY' or 'Boston, MA' are valid
def is_valid_location(_string):
    match_obj = re.match(r'([^,]+),\s*(\w{2})$', _string, re.I)
    return match_obj is not None


# return a tuple [city, state] if location string is valid
def extract_city_state(_string):
    match_obj = re.match(r'([^,]+),\s*(\w{2})$', _string, re.I)
    if match_obj is None:
        raise ValidationError(f'string "{_string}" is not a valid representation of US city')
    else:
        city = re.sub('\s+', '_', match_obj.group(1))
        state = match_obj.group(2)
        return city, state


# test sub string, case insensitive
def contains(_string, _pattern):
    return _pattern.lower() in _string.lower()

