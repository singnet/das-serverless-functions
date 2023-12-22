from actions import ActionType
from tests.integration.handle.base_test_action import BaseTestHandlerAction
import pytest


class TestQueryAction(BaseTestHandlerAction):
    @pytest.fixture
    def action_type(self):
        return ActionType.QUERY

    @pytest.fixture
    def valid_event(self, action_type):
        return {
            "body": {
                "action": action_type,
                "input": {
                    "query": {
                        "atom_type": "link",
                        "type": "Similarity",
                        "targets": [
                            {"atom_type": "node", "type": "Concept", "name": "human"},
                            {"atom_type": "node", "type": "Concept", "name": "monkey"},
                        ],
                    }
                },
            }
        }

    @pytest.fixture
    def expected_output(self):
        return [
            {
                "handle": "bad7472f41a0e7d601ca294eb4607c3a",
                "type": "Similarity",
                "template": ["Similarity", "Concept", "Concept"],
                "targets": [
                    {
                        "handle": "af12f10f9ae2002a1607ba0b47ba8407",
                        "type": "Concept",
                        "name": "human",
                    },
                    {
                        "handle": "1cdffc6b0b89ff41d68bec237481d1e1",
                        "type": "Concept",
                        "name": "monkey",
                    },
                ],
            }
        ]

    def test_ping_action(
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
