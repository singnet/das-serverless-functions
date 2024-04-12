import pytest
from actions import ActionType
from hyperon_das_atomdb.utils.expression_hasher import ExpressionHasher
from tests.integration.handle.base_test_action import BaseTestHandlerAction, human, monkey, concept, metta_type


class TestGetLinkAction(BaseTestHandlerAction):
    human_hash = ExpressionHasher.terminal_hash(concept, human)
    monkey_hash = ExpressionHasher.terminal_hash(concept, monkey)

    @pytest.fixture
    def action_type(self):
        return ActionType.GET_LINK

    @pytest.fixture
    def valid_event(self, action_type):
        return {
            "body": {
                "action": action_type,
                "input": {
                    "link_type": metta_type,
                    "link_targets": [
                        self.human_hash,
                        self.monkey_hash,
                    ],
                },
            }
        }

    def test_get_link_action(
        self,
        valid_event,
    ):
        body, status_code = self.make_request(valid_event)
        expected_status_code = 200

        assert status_code == expected_status_code, f"Unexpected status code: {status_code}. Expected: {expected_status_code}"
        assert isinstance(body, dict), "body must be a dictionary"
        assert isinstance(body.get("handle"), str), "'handle' in body must be a string."
        assert isinstance(body.get("composite_type_hash"), str), "'composite_type_hash' in body must be a string."
        assert isinstance(body.get("is_toplevel"), bool), "'is_toplevel' in body must be a boolean."
        assert isinstance(body.get("composite_type"), list), "'composite_type' in body must be a list."
        assert all(isinstance(item, str) for item in body["composite_type"]), "'composite_type' elements in body must be strings."

        assert isinstance(body.get("named_type"), str), "'named_type' in body must be a string."
        assert isinstance(body.get("named_type_hash"), str), "'named_type_hash' in body must be a string."

        assert isinstance(body.get("targets"), list), "'targets' in body must be a list."
        assert all(isinstance(item, str) for item in body["targets"]), "'targets' elements in body must be strings."

        assert isinstance(body.get("type"), str), "'type' in body must be a string."

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
