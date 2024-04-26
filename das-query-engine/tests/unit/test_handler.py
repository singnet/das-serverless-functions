from unittest.mock import patch
import pytest
from exceptions import PayloadMalformed
from unittest.mock import MagicMock
from exceptions import PayloadMalformed, UnknownActionDispatcher

patch('utils.dotenv.load_env').start()
logger_mock = patch('hyperon_das.logger.logger').start()
validate_payload_mock = patch('validators.validate').start()
action_dispatcher_mock = patch('action_dispatcher.ActionDispatcher').start()

from handler import handle, _response


@pytest.mark.parametrize("http_code_response, headers, result", [
    (200, {"Content-Type": "application/json"}, {}),
    (500, {"Content-Type": "application/json"}, {}),
    (404, {"Content-Type": "text/plain"}, ""),
])
def test_response(http_code_response, headers, result):
    r = _response(http_code_response, result, headers)

    assert isinstance(r, dict)
    assert r.get("statusCode") == http_code_response
    assert r.get("headers") == headers
    assert r.get("body") == result
    logger_mock.assert_called()


def test_handle_malformed_payload_action():
    payload = {}

    validate_payload_mock.side_effect = PayloadMalformed(message="Exception at validate: payload malformed")

    result = handle(payload)

    assert isinstance(result, dict)
    assert result.get("statusCode") == 400
    assert "headers" in result
    assert "body" in result


def test_handle_invalid_action():
    payload = {
        "action": "not_exists",
        "input": {}
    }

    validate_payload_mock.side_effect = lambda _, body: body
    action_dispatcher_mock.side_effect = UnknownActionDispatcher("unknown action")

    result = handle(payload)

    assert isinstance(result, dict)
    assert result.get("statusCode") == 404
    assert "headers" in result
    assert "body" in result
