import pytest
from actions import ActionType
from hyperon_das_atomdb.database import Node
from tests.integration.handle.base_test_action import BaseTestHandlerAction, human, symbol


class TestGetNodeAction(BaseTestHandlerAction):
    @pytest.fixture
    def action_type(self):
        return ActionType.GET_NODE

    @pytest.fixture
    def valid_event(self, action_type):
        return {
            "body": {
                "action": action_type,
                "input": {"node_type": symbol, "node_name": human},
            }
        }

    def test_get_node_action(
        self,
        valid_event,
    ):
        body, status_code = self.make_request(valid_event)
        expected_status_code = 200

        assert (
            status_code == expected_status_code
        ), f"Unexpected status code: {status_code}. Expected: {expected_status_code}"
        assert isinstance(body, Node), "body must be a Node instance"
        assert isinstance(body.handle, str), "'handle' in body must be a string."
        assert isinstance(
            body.composite_type_hash, str
        ), "'composite_type_hash' in body must be a string."
        assert isinstance(body.name, str), "'name' in body must be a string."
        assert isinstance(body.named_type, str), "'named_type' in body must be a string."

        # TODO: Uncomment when 'is_literal' is added as a custom attribute to Atom
        # See: https://github.com/singnet/das-query-engine/issues/358
        # assert isinstance(
        #     body.custom_attributes.get("is_literal"), bool
        # ), "'is_literal' in custom_attributes must be a boolean."

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
