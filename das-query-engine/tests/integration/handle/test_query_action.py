import pytest
from actions import ActionType
from hyperon_das.utils import QueryAnswer
from tests.integration.handle.base_test_action import (
    BaseTestHandlerAction,
    expression,
    inheritance,
    similarity,
    human,
    mammal,
    symbol,
)


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
                        "type": expression,
                        "targets": [
                            {"atom_type": "node", "type": symbol, "name": inheritance},
                            {"atom_type": "variable", "name": "$v1"},
                            {"atom_type": "node", "type": symbol, "name": mammal},
                        ],
                    },
                },
            }
        }
    
    @pytest.fixture
    def query_list(self, action_type):
        return {
            "body": {
                "action": action_type,
                "input": {
                    "query": [
                        {
                            "atom_type": "link",
                            "type": expression,
                            "targets": [
                                {"atom_type": "node", "type": symbol, "name": inheritance},
                                {"atom_type": "variable", "name": "$v1"},
                                {"atom_type": "node", "type": symbol, "name": mammal},
                            ],
                        },
                        {
                            "atom_type": "link",
                            "type": expression,
                            "targets": [
                                {"atom_type": "node", "type": symbol, "name": similarity},
                                {"atom_type": "variable", "name": "$v1"},
                                {"atom_type": "node", "type": symbol, "name": human},
                            ],
                        }
                    ]
                },
            }
        }

    @pytest.mark.parametrize("query_input", ["valid_event", "query_list"])
    def test_query_action(
        self,
        request,
        query_input,
    ):
        query_data = request.getfixturevalue(query_input)
        body, status_code = self.make_request(query_data)
        expected_status_code = 200

        assert (
            status_code == expected_status_code
        ), f"Assertion failed:\nReceived: {status_code}\nExpected: {expected_status_code}"

        assert isinstance(body, list), "body must be a list."
        assert len(body) > 0, "body must not be empty."
        assert all(
            isinstance(item, QueryAnswer) for item in body
        ), "All items in body must be a QueryAnswer instance."

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
