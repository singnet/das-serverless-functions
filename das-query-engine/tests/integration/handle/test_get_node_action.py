import pytest
from actions import ActionType
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

        assert status_code == expected_status_code, f"Unexpected status code: {status_code}. Expected: {expected_status_code}"
        assert isinstance(body, dict), "body must be a dictionary"
        assert isinstance(body.get("handle"), str), "'handle' in body must be a string."
        assert isinstance(body.get("composite_type_hash"), str), "'composite_type_hash' in body must be a string."
        assert isinstance(body.get("name"), str), "'name' in body must be a string."
        assert isinstance(body.get("named_type"), str), "'named_type' in body must be a string."
        assert isinstance(body.get("type"), str), "'type' in body must be a string."
        assert isinstance(body.get("is_literal"), bool), "'is_literal' in body must be a boolean."
        

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
