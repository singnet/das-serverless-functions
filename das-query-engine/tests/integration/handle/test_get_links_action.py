import pytest
from actions import ActionType
from tests.integration.handle.base_test_action import BaseTestHandlerAction, metta_type, expression


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
                    "kwargs": {
                        "cursor": 0
                    },
                    "target_types": [
                        metta_type,
                        metta_type,
                        metta_type,
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

        assert status_code == expected_status_code, f"Unexpected status code: {status_code}. Expected: {expected_status_code}"

        assert isinstance(body, list), "body must be a list."
        assert len(body) > 0
        assert all(isinstance(item, dict) for item in body), "elements in body must be dicts."


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
