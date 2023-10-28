import json
from incoming import PayloadValidator


def validate(validator: PayloadValidator, payload: any) -> any:
    result, errors = validator.validate(payload)
    assert result and errors is None, "Validation failed.\n%s" % json.dumps(
        errors,
        indent=2,
    )

    return payload
