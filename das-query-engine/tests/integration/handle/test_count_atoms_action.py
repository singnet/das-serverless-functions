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

    @pytest.fixture
    def expected_output(self):
        return [14, 26]

    def test_count_atoms_action(
        self,
        valid_event,
        expected_output,
    ):
        self.assert_successful_execution(valid_event, expected_output)

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
