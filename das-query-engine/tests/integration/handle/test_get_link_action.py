from actions import ActionType
from tests.integration.handle.base_test_action import BaseTestHandlerAction
from hyperon_das_atomdb.utils.expression_hasher import ExpressionHasher
import pytest


class TestGetLinkAction(BaseTestHandlerAction):
    @pytest.fixture
    def action_type(self):
        return ActionType.GET_LINK

    @pytest.fixture
    def valid_event(self, action_type):
        human_handle = ExpressionHasher.terminal_hash("Concept", "human")
        monkey_handle = ExpressionHasher.terminal_hash("Concept", "monkey")

        return {
            "body": {
                "action": action_type,
                "input": {
                    "link_type": "Similarity",
                    "link_targets": [human_handle, monkey_handle],
                },
            }
        }

    @pytest.fixture
    def expected_output(self):
        return {
            "handle": "ee1c03e6d1f104ccd811cfbba018451a",
            "composite_type_hash": "41c082428b28d7e9ea96160f7fd614ad",
            "is_toplevel": True,
            "composite_type": [
                "e40489cd1e7102e35469c937e05c8bba",
                "d99a604c79ce3c2e76a2f43488d5d4c3",
                "d99a604c79ce3c2e76a2f43488d5d4c3",
            ],
            "named_type": "Inheritance",
            "named_type_hash": "e40489cd1e7102e35469c937e05c8bba",
            "targets": [
                "4e8e26e3276af8a5c2ac2cc2dc95c6d2",
                "80aff30094874e75028033a38ce677bb",
            ],
        }

    def test_get_link_action(
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
