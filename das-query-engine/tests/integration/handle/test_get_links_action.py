import pytest
from actions import ActionType
from tests.integration.handle.base_test_action import BaseTestHandlerAction, expression, symbol


class TestGetLinksAction(BaseTestHandlerAction):
    @pytest.fixture
    def action_type(self):
        return ActionType.GET_LINKS

    @pytest.fixture
    def valid_event(self, action_type):
        return {
            "body": {
                "action": action_type,
                "input": {
                    "link_type": expression,
                    "target_types": [
                        symbol,
                        symbol,
                        symbol,
                    ],
                },
            }
        }

    def test_get_links_action(
        self,
        valid_event,
    ):
        body, status_code = self.make_request(valid_event)
        expected_status_code = 200

        assert (
            status_code == expected_status_code
        ), f"Unexpected status code: {status_code}. Expected: {expected_status_code}"

        assert isinstance(body, list)
        assert len(body) > 0
        assert all(isinstance(item, dict) for item in body), "elements in body must be dicts."

        link = body[0]

        assert isinstance(link.get("handle"), str), "'handle' in link must be a string."
        assert isinstance(link.get("type"), str), "'type' in link must be a string."
        assert isinstance(
            link.get("composite_type_hash"), str
        ), "'composite_type_hash' in link must be a string."
        assert isinstance(link.get("is_toplevel"), bool), "'is_toplevel' in link must be a boolean."
        assert isinstance(
            link.get("composite_type"), list
        ), "'composite_type' in link must be a list."
        assert all(
            isinstance(item, str) for item in link.get("composite_type")
        ), "'composite_type' elements in link must be strings."
        assert isinstance(link.get("named_type"), str), "'named_type' in link must be a string."
        assert isinstance(
            link.get("named_type_hash"), str
        ), "'named_type_hash' in link must be a string."
        assert isinstance(link.get("targets"), list), "'targets' in link must be a list."
        assert all(
            isinstance(item, str) for item in link.get("targets")
        ), "'targets' elements in link must be strings."

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
