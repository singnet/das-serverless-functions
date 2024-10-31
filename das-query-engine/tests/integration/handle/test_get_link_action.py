import pytest
from actions import ActionType
from hyperon_das_atomdb.database import Link
from tests.integration.handle.base_test_action import BaseTestHandlerAction, expression


class TestGetLinkAction(BaseTestHandlerAction):
    @pytest.fixture
    def action_type(self):
        return ActionType.GET_LINK

    @pytest.fixture
    def valid_event(self, action_type):
        return {
            "body": {
                "action": action_type,
                "input": {
                    "link_type": expression,
                    "link_targets": [
                        "0ca31260e280b30d70238d08e150b78d",
                        "ae7ab1a9791ca0dcbf54ca7955bbdbc9",
                        "6872b1cd2cfbc483ac52687852e5f1ad",
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

        assert (
            status_code == expected_status_code
        ), f"Unexpected status code: {status_code}. Expected: {expected_status_code}"
        assert isinstance(body, Link), "body must be a Link instance"
        assert isinstance(body.handle, str), "'handle' in body must be a string."
        assert isinstance(
            body.composite_type_hash, str
        ), "'composite_type_hash' in body must be a string."
        assert isinstance(body.is_toplevel, bool), "'is_toplevel' in body must be a boolean."
        assert isinstance(body.composite_type, list), "'composite_type' in body must be a list."
        assert all(
            isinstance(item, str) for item in body.composite_type
        ), "'composite_type' elements in body must be strings."

        assert isinstance(body.named_type, str), "'named_type' in body must be a string."
        assert isinstance(body.named_type_hash, str), "'named_type_hash' in body must be a string."

        assert isinstance(body.targets, list), "'targets' in body must be a list."
        assert all(
            isinstance(item, str) for item in body.targets
        ), "'targets' elements in body must be strings."

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
