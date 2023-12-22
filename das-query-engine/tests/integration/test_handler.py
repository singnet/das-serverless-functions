import json
import pytest
from handler import (
    handle,
    PayloadMalformed,
    UnknownActionDispatcher,
    UnreachableConnection,
)
from actions import ActionType
import os
from dotenv import load_dotenv


@pytest.fixture(autouse=True)
def load_env_variables():
    env_path = ".env.testing"
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)


class TestPingAction:
    @pytest.fixture
    def valid_event(self):
        return {
            "body": {
                "action": ActionType.PING,
                "input": {},
            }
        }

    @pytest.fixture
    def malformed_event(self):
        return {"body": {}}

    @pytest.fixture
    def unknown_action_event(self):
        return {"body": {"action": "unknown_action", "input": {}}}

    def test_successful_execution(self, valid_event):
        expected_output = json.dumps({"message": "pong"})
        response = handle(valid_event, context={})
        assert response["statusCode"] == 200
        assert response["body"] == expected_output

    def test_payload_malformed(self, malformed_event):
        response = handle(malformed_event, context={})
        assert response["statusCode"] == 400

    def test_unknown_action_dispatcher(self, unknown_action_event):
        response = handle(unknown_action_event, context={})
        assert response["statusCode"] == 404

    def test_unexpected_exception(self, mocker, valid_event):
        mocker.patch(
            "action_dispatcher.ActionDispatcher.dispatch",
            side_effect=UnreachableConnection("Connection failed"),
        )
        response = handle(valid_event, context={})
        assert response["statusCode"] == 500


class TestCountAtomsAction:
    @pytest.fixture
    def valid_event(self):
        return {
            "body": {
                "action": ActionType.COUNT_ATOMS,
                "input": {},
            }
        }

    @pytest.fixture
    def malformed_event(self):
        return {"body": {}}

    @pytest.fixture
    def unknown_action_event(self):
        return {"body": {"action": "unknown_action", "input": {}}}

    def test_successful_execution(self, valid_event):
        expected_output = json.dumps([14, 26])
        response = handle(valid_event, context={})
        assert response["statusCode"] == 200
        assert response["body"] == expected_output

    def test_payload_malformed(self, malformed_event):
        response = handle(malformed_event, context={})
        assert response["statusCode"] == 400

    def test_unknown_action_dispatcher(self, unknown_action_event):
        response = handle(unknown_action_event, context={})
        assert response["statusCode"] == 404

    def test_unexpected_exception(self, mocker, valid_event):
        mocker.patch(
            "action_dispatcher.ActionDispatcher.dispatch",
            side_effect=UnreachableConnection("Connection failed"),
        )
        response = handle(valid_event, context={})
        assert response["statusCode"] == 500


# class TestGetLinkAction:
#     @pytest.fixture
#     def valid_event(self):
#         return {
#             "body": {
#                 "action": ActionType.COUNT_ATOMS,
#                 "input": {},
#             }
#         }

#     @pytest.fixture
#     def malformed_event(self):
#         return {"body": {}}

#     @pytest.fixture
#     def unknown_action_event(self):
#         return {"body": {"action": "unknown_action", "input": {}}}

#     def test_successful_execution(self, valid_event):
#         expected_output = json.dumps([14, 26])
#         response = handle(valid_event, context={})
#         assert response["statusCode"] == 200
#         assert response["body"] == expected_output

#     def test_payload_malformed(self, malformed_event):
#         response = handle(malformed_event, context={})
#         assert response["statusCode"] == 400

#     def test_unknown_action_dispatcher(self, unknown_action_event):
#         response = handle(unknown_action_event, context={})
#         assert response["statusCode"] == 404

#     def test_unexpected_exception(self, mocker, valid_event):
#         mocker.patch(
#             "action_dispatcher.ActionDispatcher.dispatch",
#             side_effect=UnreachableConnection("Connection failed"),
#         )
#         response = handle(valid_event, context={})
#         assert response["statusCode"] == 500
