from incoming import datatypes, PayloadValidator
from validators.custom_validator_types import validate_dict


class EventValidator(PayloadValidator):
    action = datatypes.String()
    input = datatypes.Function(validate_dict)
