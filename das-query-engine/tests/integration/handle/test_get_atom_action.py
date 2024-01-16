import pytest
from actions import ActionType
from hyperon_das_atomdb.utils.expression_hasher import ExpressionHasher
from tests.integration.handle.base_test_action import BaseTestHandlerAction


class TestGetAtomAction(BaseTestHandlerAction):
    named_type = "Concept"
    terminal_name = "human"
    human_handle = ExpressionHasher.terminal_hash(named_type, terminal_name)

    @pytest.fixture
    def action_type(self):
        return ActionType.GET_ATOM

    @pytest.fixture
    def valid_event(self, action_type):
        return {
            "body": {
                "action": action_type,
                "input": {
                    "handle": self.human_handle,
                },
            }
        }

    @pytest.fixture
    def expected_output(self):
        return {
            "handle": self.human_handle,
            "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
            "name": self.terminal_name,
            "named_type": self.named_type,
        }

    def test_get_atom_action(
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
