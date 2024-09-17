import pytest
from actions import ActionType
from hyperon_das_atomdb.utils.expression_hasher import ExpressionHasher
from tests.integration.handle.base_test_action import BaseTestHandlerAction, human, symbol


class TestGetIncomingLinksAction(BaseTestHandlerAction):
    human_handle = ExpressionHasher.terminal_hash(symbol, human)

    @pytest.fixture
    def action_type(self):
        return ActionType.GET_INCOMING_LINKS

    @pytest.fixture
    def valid_event(self, action_type):
        return {
            "body": {
                "action": action_type,
                "input": {
                    "atom_handle": self.human_handle,
                    "kwargs": {"targets_document": True, "no_iterator": True},
                },
            }
        }

    def test_incoming_links_action(
        self,
        valid_event,
    ):
        body, status_code = self.make_request(valid_event)
        expected_status_code = 200

        assert (
            status_code == expected_status_code
        ), f"Unexpected status code: {status_code}. Expected: {expected_status_code}"
        assert isinstance(body, list), "body must be a tuple."
        items = body
        assert len(items) == 8, "body must contain eight elements."

        for item in items:
            assert isinstance(item, dict), "Each item in body must be a dict."
            # assert len(item) == x, "List in body must contain x elements."

            assert isinstance(
                item.get("handle"), str
            ), "'handle' in item must be a string."
            assert isinstance(item.get("type"), str), "'type' in item must be a string."
            assert isinstance(
                item.get("composite_type_hash"), str
            ), "'composite_type_hash' in item must be a string."
            assert isinstance(
                item.get("is_toplevel"), bool
            ), "'is_toplevel' in item must be a boolean."
            assert isinstance(
                item.get("composite_type"), list
            ), "'composite_type' in item must be a list of strings."
            assert all(
                isinstance(item, str) for item in item.get("composite_type")
            ), "'composite_type' elements in item must be strings."
            assert isinstance(
                item.get("named_type"), str
            ), "'named_type' in item must be a string."
            assert isinstance(
                item.get("named_type_hash"), str
            ), "'named_type_hash' in item must be a string."
            assert isinstance(
                item.get("targets"), list
            ), "'targets' in item must be a list of strings."
            assert all(
                isinstance(item, str) for item in item.get("targets")
            ), "'targets' elements in item must be strings."
            assert isinstance(
                item.get("targets_document"), list
            ), "'targets_document' in item must be a list of dictionaries."

            for atom in item.get("targets_document"):
                assert isinstance(atom, dict), f"{type(atom)} is not a dictionary."
                assert isinstance(atom.get("handle"), str), "'handle' in atom must be a string."
                assert isinstance(atom.get("type"), str), "'type' in atom must be a string."
                assert isinstance(
                    atom.get("composite_type_hash"), str
                ), "'composite_type_hash' in atom must be a string."
                assert isinstance(atom.get("name"), str), "'name' in atom must be a string."
                assert isinstance(
                    atom.get("named_type"), str
                ), "'named_type' in atom must be a string."
                assert isinstance(
                    atom.get("is_literal"), bool
                ), "'is_literal' in atom must be a boolean."

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
