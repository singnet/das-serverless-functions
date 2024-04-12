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

        assert isinstance(body, list)
        assert len(body) > 0
        assert all((isinstance(item, tuple), f"{type(item)}") for item in body)

        for item in body:
            assert len(item) == 2
            assignment, query_answer = item

            assert isinstance(assignment, Assignment)
            assert isinstance(query_answer, dict)

            assert isinstance(query_answer.get("handle"), str)
            assert isinstance(query_answer.get("type"), str)
            assert isinstance(query_answer.get("composite_type_hash"), str)
            assert isinstance(query_answer.get("is_toplevel"), bool)
            assert isinstance(query_answer.get("composite_type"), list)
            assert all((isinstance(item, str)) for item in query_answer.get("composite_type"))

            assert isinstance(query_answer.get("named_type"), str)
            assert isinstance(query_answer.get("named_type_hash"), str)
            assert isinstance(query_answer.get("targets"), list)

            targets = query_answer["targets"]

            for target in targets:
                assert isinstance(target, dict)
                assert isinstance(target.get("handle"), str)
                assert isinstance(target.get("type"), str)
                assert isinstance(target.get("composite_type_hash"), str)
                assert isinstance(target.get("name"), str)
                assert isinstance(target.get("named_type"), str)
                assert isinstance(target.get("is_literal"), bool)



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
