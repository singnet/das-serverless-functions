import pytest
from actions import ActionType
from tests.integration.handle.base_test_action import BaseTestHandlerAction, expression, symbol, mammal, inheritance
from hyperon_das.das import Assignment


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

    def test_query_action(
        self,
        valid_event,
    ):
        body, status_code = self.make_request(valid_event)
        expected_status_code = 200

        assert status_code == expected_status_code, \
            f"Assertion failed:\nReceived: {status_code}\nExpected: {expected_status_code}"

        assert isinstance(body, list), "body must be a list."
        assert len(body) > 0, "body must not be empty."
        assert all(isinstance(item, tuple) for item in body), "All items in body must be tuples."

        for item in body:
            assert len(item) == 2, "Each item in body must contain two elements."
            assignment, query_answer = item

            assert isinstance(assignment, Assignment), "Assignment must be an instance of Assignment."
            assert isinstance(query_answer, dict), "query_answer must be a dictionary."

            assert isinstance(query_answer.get("handle"), str), "'handle' in query_answer must be a string."
            assert isinstance(query_answer.get("type"), str), "'type' in query_answer must be a string."
            assert isinstance(query_answer.get("composite_type_hash"), str), "'composite_type_hash' in query_answer must be a string."
            assert isinstance(query_answer.get("is_toplevel"), bool), "'is_toplevel' in query_answer must be a boolean."
            assert isinstance(query_answer.get("composite_type"), list), "'composite_type' in query_answer must be a list."
            assert all(isinstance(item, str) for item in query_answer.get("composite_type")), "'composite_type' elements in query_answer must be strings."
            assert isinstance(query_answer.get("named_type"), str), "'named_type' in query_answer must be a string."
            assert isinstance(query_answer.get("named_type_hash"), str), "'named_type_hash' in query_answer must be a string."
            assert isinstance(query_answer.get("targets"), list), "'targets' in query_answer must be a list."

            targets = query_answer["targets"]

            for target in targets:
                assert isinstance(target, dict), "Each target must be a dictionary."
                assert isinstance(target.get("handle"), str), "'handle' in target must be a string."
                assert isinstance(target.get("type"), str), "'type' in target must be a string."
                assert isinstance(target.get("composite_type_hash"), str), "'composite_type_hash' in target must be a string."
                assert isinstance(target.get("name"), str), "'name' in target must be a string."
                assert isinstance(target.get("named_type"), str), "'named_type' in target must be a string."
                assert isinstance(target.get("is_literal"), bool), "'is_literal' in target must be a boolean."




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
