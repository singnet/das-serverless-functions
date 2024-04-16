import pytest
from actions import ActionType
from tests.integration.handle.base_test_action import BaseTestHandlerAction, symbol, human
from hyperon_das_atomdb.utils.expression_hasher import ExpressionHasher


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
                    "kwargs": {
                        "targets_document": True,
                        "no_iterator": True
                    },
                },
            }
        }


    def test_incoming_links_action(
        self,
        valid_event,
    ):
        body, status_code = self.make_request(valid_event)
        expected_status_code = 200

        assert status_code == expected_status_code, f"Unexpected status code: {status_code}. Expected: {expected_status_code}"
        assert isinstance(body, list), "body must be a list."
        assert len(body) > 0, "body must contain at least one element."

        
        for item in body:
            assert isinstance(item, tuple), "Each item in body must be a tuple."
            assert len(item) == 2, "Each tuple in body must contain two elements."

            item_dict, item_tuple = item
            assert isinstance(item_dict, dict), "First element of tuple must be a dictionary."
            assert isinstance(item_tuple, list), "Second element of tuple must be a list."

            assert isinstance(item_dict.get("handle"), str), "'handle' in item_dict must be a string."
            assert isinstance(item_dict.get("type"), str), "'type' in item_dict must be a string."
            assert isinstance(item_dict.get("composite_type_hash"), str), "'composite_type_hash' in item_dict must be a string."
            assert isinstance(item_dict.get("is_toplevel"), bool), "'is_toplevel' in item_dict must be a boolean."
            assert isinstance(item_dict.get("composite_type"), list), "'composite_type' in item_dict must be a list of strings."
            assert all(isinstance(item, str) for item in item_dict.get("composite_type")), "'composite_type' elements in item_dict must be strings."
            assert isinstance(item_dict.get("named_type"), str), "'named_type' in item_dict must be a string."
            assert isinstance(item_dict.get("named_type_hash"), str), "'named_type_hash' in item_dict must be a string."
            assert isinstance(item_dict.get("targets"), list), "'targets' in item_dict must be a list of strings."
            assert all(isinstance(item, str) for item in item_dict.get("targets")), "'targets' elements in item_dict must be strings."


            for atom in item_tuple:
                assert isinstance(atom, dict), f"{type(atom)} is not a dictionary."
                assert isinstance(atom.get("handle"), str), "'handle' in atom must be a string."
                assert isinstance(atom.get("type"), str), "'type' in atom must be a string."
                assert isinstance(atom.get("composite_type_hash"), str), "'composite_type_hash' in atom must be a string."
                assert isinstance(atom.get("name"), str), "'name' in atom must be a string."
                assert isinstance(atom.get("named_type"), str), "'named_type' in atom must be a string."
                assert isinstance(atom.get("is_literal"), bool), "'is_literal' in atom must be a boolean."



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
