import json
from abc import ABC, abstractmethod

import pytest
from handler import UnreachableConnection, handle
@pytest.mark.skip(
    reason="Disabled because of das-serverless-function#94"
)
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

    @staticmethod
    def _sorted_nested(obj):
        if isinstance(obj, list):
            return sorted(str(BaseTestHandlerAction._sorted_nested(item)) for item in obj)
        elif isinstance(obj, dict):
            return sorted(
                (key, BaseTestHandlerAction._sorted_nested(value)) for key, value in obj.items()
            )
        elif isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        else:
            return str(obj)

    @staticmethod
    def _compare_nested(obj1, obj2):
        return BaseTestHandlerAction._sorted_nested(obj1) == BaseTestHandlerAction._sorted_nested(
            obj2
        )

    def assert_successful_execution(self, valid_event, expected_output):
        response = handle(valid_event, context={})
        body = json.loads(response["body"])
        assert response["statusCode"] == 200, f"Assertion failed:\nReceived: {response['statusCode']}\nExpected: 200"
        assert BaseTestHandlerAction._compare_nested(
            body,
            expected_output,
        ), f"Assertion failed:\nResponse Body: {response['body']}\nExpected: {json.dumps(expected_output)}"

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
