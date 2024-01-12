import pytest
from unittest.mock import MagicMock
from action_dispatcher import (
    ActionDispatcher,
    ActionType,
    UnknownActionDispatcher,
    PayloadMalformed,
)
from validators.actions import GetAtomValidator


def test_dispatch_with_validator():
    payload = dict(handle="bad7472f41a0e7d601ca294eb4607c3a")
    expected_output = {
        "handle": "bad7472f41a0e7d601ca294eb4607c3a",
        "composite_type_hash": "d99a604c79ce3c2e76a2f43488d5d4c3",
        "name": "monkey",
        "named_type": "Concept",
    }

    action_mapper = MagicMock()
    action_mapper.get_action_dispatcher.return_value = {
        "action": MagicMock(return_value=expected_output),
        "validator": GetAtomValidator,
    }

    action_dispatcher = ActionDispatcher(action_mapper)

    result = action_dispatcher.dispatch(
        ActionType.GET_ATOM,
        payload,
    )

    assert result == expected_output


def test_dispatch_without_validator():
    expected_output = [14, 26]
    action_mapper = MagicMock()
    action_mapper.get_action_dispatcher.return_value = {
        "action": MagicMock(return_value=expected_output),
        "validator": None,
    }

    action_dispatcher = ActionDispatcher(action_mapper)

    result = action_dispatcher.dispatch(ActionType.COUNT_ATOMS)

    assert result == expected_output


def test_dispatch_unknown_action_dispatcher():
    action_mapper = MagicMock()
    action_mapper.get_action_dispatcher.return_value = None

    action_dispatcher = ActionDispatcher(action_mapper)

    with pytest.raises(UnknownActionDispatcher):
        action_dispatcher.dispatch(ActionType.PING)


def test_dispatch_payload_malformed():
    action_mapper = MagicMock()
    action_mapper.get_action_dispatcher.return_value = {
        "action": MagicMock(),
        "validator": MagicMock(),
    }

    action_dispatcher = ActionDispatcher(action_mapper)

    with pytest.raises(PayloadMalformed):
        action_dispatcher.dispatch(ActionType.GET_ATOM, {"key": "value"})
