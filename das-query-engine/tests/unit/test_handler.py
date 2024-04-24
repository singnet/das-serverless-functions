from handler import handle


def test_handle_invalid_action(mocker):
    mocker.patch('utils.dotenv.load_env', lambda: None)

    payload = {"action": "INVALID_ACTION", "input": {}}

    result = handle(payload)

    assert "body" in result
