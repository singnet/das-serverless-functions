import pytest
from actions import ActionType
from tests.integration.handle.base_test_action import BaseTestHandlerAction


class TestPingAction(BaseTestHandlerAction):
    @pytest.fixture
    def action_type(self):
        return ActionType.PING

    @pytest.fixture
    def valid_event(self, action_type):
        return {
            "body": {
                "action": action_type,
                "input": {},
            }
        }

    def test_ping_action(
        self,
        valid_event,
    ):
        body, status_code = self.make_request(valid_event)
        expected_status_code = 200

        assert status_code == expected_status_code, f"Unexpected status code: {status_code}. Expected: {expected_status_code}"
        assert isinstance(body, dict), "body must be a dictionary"
        assert "message" in body, "The dictionary body must contain the key 'message'"
        assert body["message"] == "pong", "The value of the key 'message' in body must be 'pong'"


    def test_malformed_payload(self, malformed_event):
        self.assert_payload_malformed(malformed_event)

    def test_unknown_action(self, unknown_action_event):
        self.assert_unknown_action_dispatcher(unknown_action_event)

    def test_unexpected_exception(
        self,
        mocker,
        valid_event,
    ):
        self.assert_unexpected_exception(mocker, valid_event)
