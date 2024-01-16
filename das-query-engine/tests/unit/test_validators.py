from validators.custom_validator_types import validate_dict


def test_validate_dict_empty():
    assert validate_dict({}) is True


def test_validate_dict_non_empty():
    assert validate_dict({"key": "value"}) is True


def test_validate_dict_invalid_input():
    assert validate_dict("not a dict") is False


def test_validate_dict_none_input():
    assert validate_dict(None) is False


def test_validate_dict_with_args():
    assert validate_dict({}, 1, 2, 3) is True


def test_validate_dict_with_kwargs():
    assert validate_dict({}, key="value") is True
