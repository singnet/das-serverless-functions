from handler import handle


def test_handle_invalid_action():
    payload = {"action": "INVALID_ACTION", "input": {}}
    result = handle(payload)

    assert "body" in result
