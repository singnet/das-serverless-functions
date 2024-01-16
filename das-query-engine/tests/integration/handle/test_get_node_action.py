from actions import ActionType
from tests.integration.handle.base_test_action import BaseTestHandlerAction
from hyperon_das_atomdb.utils.expression_hasher import ExpressionHasher
import pytest


class TestGetNodeAction(BaseTestHandlerAction):
    @pytest.fixture
    def action_type(self):
        return ActionType.GET_NODE

    @pytest.fixture
    def valid_event(self, action_type):
        return {
            "body": {
                "action": action_type,
                "input": {"node_type": "Concept", "node_name": "human"},
            }
        }

    @pytest.fixture
    def expected_output(self):
        human_handle = ExpressionHasher.terminal_hash("Concept", "human")

        return {
            "handle": human_handle,
            "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
            "name": "human",
            "named_type": "Concept",
        }

    def test_get_node_action(
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
