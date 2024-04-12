import pytest
from actions import ActionType
from tests.integration.handle.base_test_action import BaseTestHandlerAction
from hyperon_das import DistributedAtomSpace


class TestHandshakeAction(BaseTestHandlerAction):
    @pytest.fixture
    def action_type(self):
        return ActionType.HANDSHAKE


    @pytest.fixture
    def valid_event(self, action_type):
        on_premises = DistributedAtomSpace.about()
        on_premises_das_version = on_premises["das"]["version"]
        on_premises_atomdb_version = on_premises["atom_db"]["version"]

        return {
            "body": {
                "action": action_type,
                "input": {
                    "das_version": on_premises_das_version,
                    "atomdb_version": on_premises_atomdb_version,
                },
            }
        }

    def test_handshake_action(
        self,
        valid_event,
    ):
        body, status_code = self.make_request(valid_event)
        expected_status_code = 200

        assert status_code == expected_status_code, f"Unexpected status code: {status_code}. Expected: {expected_status_code}"
        assert isinstance(body, dict), "body must be a dictionary"
        assert isinstance(body.get("das"), dict), "'das' in body must be a dictionary."
        assert isinstance(body.get("atom_db"), dict), "'atom_db' in body must be a dictionary."

        assert isinstance(body["das"].get("name"), str), "'name' in 'das' must be a string."
        assert isinstance(body["das"].get("version"), str), "'version' in 'das' must be a string."
        assert isinstance(body["das"].get("summary"), str), "'summary' in 'das' must be a string."

        assert isinstance(body["atom_db"].get("name"), str), "'name' in 'atom_db' must be a string."
        assert isinstance(body["atom_db"].get("version"), str), "'version' in 'atom_db' must be a string."
        assert isinstance(body["atom_db"].get("summary"), str), "'summary' in 'atom_db' must be a string."


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
