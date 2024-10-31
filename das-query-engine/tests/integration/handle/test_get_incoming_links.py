import pytest
from actions import ActionType
from hyperon_das_atomdb.database import Link, Node
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
            assert isinstance(item, Link), "Each item in body must be a Link instance."

            assert isinstance(item.handle, str), "'handle' in item must be a string."
            assert isinstance(
                item.composite_type_hash, str
            ), "'composite_type_hash' in item must be a string."
            assert isinstance(item.is_toplevel, bool), "'is_toplevel' in item must be a boolean."
            assert isinstance(
                item.composite_type, list
            ), "'composite_type' in item must be a list of strings."
            assert all(
                isinstance(item, str) for item in item.composite_type
            ), "'composite_type' elements in item must be strings."
            assert isinstance(item.named_type, str), "'named_type' in item must be a string."
            assert isinstance(
                item.named_type_hash, str
            ), "'named_type_hash' in item must be a string."
            assert isinstance(item.targets, list), "'targets' in item must be a list of strings."
            assert all(
                isinstance(item, str) for item in item.targets
            ), "'targets' elements in item must be strings."
            assert isinstance(
                item.targets_documents, list
            ), "'targets_documents' in item must be a list of Atoms instances (Nodes or Links)."

            for atom in item.targets_documents:
                assert isinstance(atom, (Node, Link)), f"{type(atom)} is not a Node or Link."
                assert isinstance(atom.handle, str), "'handle' in atom must be a string."
                assert isinstance(
                    atom.composite_type_hash, str
                ), "'composite_type_hash' in atom must be a string."
                assert isinstance(atom.name, str), "'name' in atom must be a string."
                assert isinstance(atom.named_type, str), "'named_type' in atom must be a string."

                # TODO: Uncomment when 'is_literal' is added as a custom attribute to Atom
                # See: https://github.com/singnet/das-query-engine/issues/358
                # assert isinstance(
                #     atom.custom_attributes.get("is_literal"), bool
                # ), "'is_literal' in custom attributes must be a boolean."

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
