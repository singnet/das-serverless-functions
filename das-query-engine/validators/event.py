from incoming import PayloadValidator, datatypes
from validators.custom_validator_types import validate_dict


class EventValidator(PayloadValidator):
    strict = True

    action = datatypes.String()
    input = datatypes.Function(validate_dict)
