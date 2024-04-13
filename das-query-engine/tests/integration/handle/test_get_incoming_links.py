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
        assert isinstance(body, list)
        assert len(body) > 0
        
        for item in body:
            assert isinstance(item, tuple)
            assert len(item) == 2

            item_dict, item_tuple = item

            assert isinstance(item_dict, dict)

            assert isinstance(item_dict.get("handle"), str)
            assert isinstance(item_dict.get("type"), str)
            assert isinstance(item_dict.get("composite_type_hash"), str)
            assert isinstance(item_dict.get("is_toplevel"), bool)
            assert isinstance(item_dict.get("composite_type"), list)
            assert all((isinstance(item, str)) for item in item_dict.get("composite_type"))

            assert isinstance(item_dict.get("named_type"), str)
            assert isinstance(item_dict.get("named_type_hash"), str)
            assert isinstance(item_dict.get("targets"), list)
            assert all((isinstance(item, str)) for item in item_dict.get("targets"))

            assert isinstance(item_tuple, list)

            for atom in item_tuple:
                assert isinstance(atom, dict)
                assert isinstance(atom.get("handle"), str)
                assert isinstance(atom.get("type"), str)
                assert isinstance(atom.get("composite_type_hash"), str)
                assert isinstance(atom.get("name"), str)
                assert isinstance(atom.get("named_type"), str)
                assert isinstance(atom.get("is_literal"), bool)



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
