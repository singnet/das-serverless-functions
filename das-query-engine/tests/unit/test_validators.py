from validators.custom_validator_types import validate_dict


def test_validate_dict_empty():
    assert validate_dict({}) == True


def test_validate_dict_non_empty():
    assert validate_dict({"key": "value"}) == True


def test_validate_dict_invalid_input():
    assert validate_dict("not a dict") == False


def test_validate_dict_none_input():
    assert validate_dict(None) == False


def test_validate_dict_with_args():
    assert validate_dict({}, 1, 2, 3) == True


def test_validate_dict_with_kwargs():
    assert validate_dict({}, key="value") == True
