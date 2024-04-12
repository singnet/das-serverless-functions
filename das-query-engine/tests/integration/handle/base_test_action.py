from abc import ABC, abstractmethod

import pytest
from handler import UnreachableConnection, handle

monkey = '"monkey"'
human = '"human"'
mammal = '"mammal"'


symbol = 'Symbol'
concept = 'Concept'
similarity = 'Similarity'
metta_type = 'MettaType'
expression = 'Expression'


class BaseTestHandlerAction(ABC):
    @abstractmethod
    def action_type(self):
        pass

    @abstractmethod
    def valid_event(self, action_type):
        pass

    @pytest.fixture
    def malformed_event(self):
        return {"body": {}}

    @pytest.fixture
    def unknown_action_event(self):
        return {"body": {"action": "unknown_action", "input": {}}}

    def make_request(self, valid_event):
        response = handle(valid_event, context={})
        body = response["body"]
        status_code = response["statusCode"]

        return body, status_code

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
