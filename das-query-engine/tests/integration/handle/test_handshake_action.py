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

    @pytest.fixture
    def expected_output(self):
        return {"ok": True}

    def test_handshake_action(
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
