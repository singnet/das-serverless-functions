import pytest
from actions import ActionType
from hyperon_das_atomdb.utils.expression_hasher import ExpressionHasher
from tests.integration.handle.base_test_action import BaseTestHandlerAction


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
            "handle": "bad7472f41a0e7d601ca294eb4607c3a",
            "composite_type_hash": "ed73ea081d170e1d89fc950820ce1cee",
            "is_toplevel": True,
            "composite_type": [
                "a9dea78180588431ec64d6bc4872fdbc",
                "d99a604c79ce3c2e76a2f43488d5d4c3",
                "d99a604c79ce3c2e76a2f43488d5d4c3",
            ],
            "named_type": "Similarity",
            "named_type_hash": "a9dea78180588431ec64d6bc4872fdbc",
            "targets": [
                "af12f10f9ae2002a1607ba0b47ba8407",
                "1cdffc6b0b89ff41d68bec237481d1e1",
            ],
            "type": "Similarity",
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
