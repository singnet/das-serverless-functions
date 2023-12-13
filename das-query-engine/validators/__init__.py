import json
from incoming import PayloadValidator
from exceptions import PayloadMalformed


def validate(validator: PayloadValidator, payload: any) -> any:
    try:
        result, errors = validator.validate(payload)
        assert result and errors is None, "Validation failed.\n%s" % json.dumps(
            errors,
            indent=2,
        )

        return payload
    except Exception as e:
        raise PayloadMalformed(
            message=f"Exception at validate: payload malformed",
            details=str(e),
        )
