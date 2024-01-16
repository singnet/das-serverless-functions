import pytest
from abc import ABC, abstractmethod
from handler import handle, UnreachableConnection
import json


class BaseTestHandlerAction(ABC):
    @abstractmethod
    def action_type(self):
        pass

    @abstractmethod
    def valid_event(self, action_type):
        pass

    @abstractmethod
    def expected_output(self):
        pass

    @pytest.fixture
    def malformed_event(self):
        return {"body": {}}

    @pytest.fixture
    def unknown_action_event(self):
        return {"body": {"action": "unknown_action", "input": {}}}

    def assert_successful_execution(self, valid_event, expected_output):
        response = handle(valid_event, context={})
        assert response["statusCode"] == 200
        assert response["body"] == json.dumps(expected_output)

    def assert_payload_malformed(self, malformed_event):
        response = handle(malformed_event, context={})
        assert response["statusCode"] == 400

    def assert_unknown_action_dispatcher(self, unknown_action_event):
        response = handle(unknown_action_event, context={})
        assert response["statusCode"] == 404

    def assert_unexpected_exception(self, mocker, valid_event):
        mocker.patch(
            "action_dispatcher.ActionDispatcher.dispatch",
            side_effect=UnreachableConnection("Connection failed"),
        )
        response = handle(valid_event, context={})
        assert response["statusCode"] == 500
