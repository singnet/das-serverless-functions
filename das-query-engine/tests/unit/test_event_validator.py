from validators.event import EventValidator


def test_event_validator_valid_payload():
    payload = {"action": "some_action", "input": {"key": "value"}}

    validator = EventValidator()
    result, errors = validator.validate(payload)

    assert result is not None
    assert errors is None


def test_event_validator_invalid_payload():
    payload = {"action": 123, "input": "invalid_input"}

    validator = EventValidator()
    result, errors = validator.validate(payload)

    assert result is False
    assert errors is not None
