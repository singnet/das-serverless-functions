from actions import ActionType
from tests.integration.handle.base_test_action import BaseTestHandlerAction
import pytest


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
                    "link_type": "Inheritance",
                    "link_targets": [
                        "4e8e26e3276af8a5c2ac2cc2dc95c6d2",
                        "80aff30094874e75028033a38ce677bb",
                    ],
                },
            }
        }

    @pytest.fixture
    def expected_output(self):
        return [
            {
                "handle": "ee1c03e6d1f104ccd811cfbba018451a",
                "type": "Inheritance",
                "template": ["Inheritance", "Concept", "Concept"],
                "targets": [
                    "4e8e26e3276af8a5c2ac2cc2dc95c6d2",
                    "80aff30094874e75028033a38ce677bb",
                ],
            }
        ]

    def test_get_links_action(
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
