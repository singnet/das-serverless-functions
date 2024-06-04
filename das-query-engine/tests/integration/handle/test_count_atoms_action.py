import pytest
from actions import ActionType
from tests.integration.handle.base_test_action import BaseTestHandlerAction


class TestCountAtomsAction(BaseTestHandlerAction):
    @pytest.fixture
    def action_type(self):
        return ActionType.COUNT_ATOMS

    @pytest.fixture
    def valid_event(self, action_type):
        return {
            "body": {
                "action": action_type,
                "input": {},
            }
        }

    def test_count_atoms_action(
        self,
        valid_event,
    ):
        body, status_code = self.make_request(valid_event)
        expected_status_code = 200

        assert (
            status_code == expected_status_code
        ), f"Assertion failed:\nReceived: {status_code}\nExpected: {expected_status_code}"

        assert isinstance(body, tuple), "body must be a tuple."
        assert all(isinstance(item, int) for item in body), "All items in body must be integers."
        assert len(body) == 2, "body must contain exactly two elements."

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
