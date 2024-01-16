import re
import pytest
from actions import ActionType
from action_mapper import ActionMapper
from unittest.mock import Mock
from exceptions import UnknownActionDispatcher


def test_build_dispatcher_ping_action():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)

    dispatchers = action_mapper._build_dispatcher()

    assert isinstance(dispatchers, dict)
    assert dispatchers[ActionType.PING]["action"] == expected_actions.ping
    assert dispatchers[ActionType.PING]["validator"] is None


def test_build_dispatcher_count_atoms_action():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)

    dispatchers = action_mapper._build_dispatcher()

    assert isinstance(dispatchers, dict)
    assert dispatchers[ActionType.COUNT_ATOMS]["action"] == expected_actions.count_atoms
    assert dispatchers[ActionType.COUNT_ATOMS]["validator"] is None


def test_build_dispatcher_get_atom_action():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)

    dispatchers = action_mapper._build_dispatcher()

    assert isinstance(dispatchers, dict)
    assert hasattr(dispatchers[ActionType.GET_ATOM]["validator"], "validate")
    assert dispatchers[ActionType.GET_ATOM]["action"] == expected_actions.get_atom


def test_build_dispatcher_get_node_action():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)

    dispatchers = action_mapper._build_dispatcher()

    assert hasattr(dispatchers[ActionType.GET_NODE]["validator"], "validate")
    assert dispatchers[ActionType.GET_NODE]["action"] == expected_actions.get_node


def test_build_dispatcher_get_link_action():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)

    dispatchers = action_mapper._build_dispatcher()

    assert hasattr(dispatchers[ActionType.GET_LINK]["validator"], "validate")
    assert dispatchers[ActionType.GET_LINK]["action"] == expected_actions.get_link


def test_build_dispatcher_get_links_action():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)

    dispatchers = action_mapper._build_dispatcher()

    assert hasattr(dispatchers[ActionType.GET_LINKS]["validator"], "validate")
    assert dispatchers[ActionType.GET_LINKS]["action"] == expected_actions.get_links


def test_build_dispatcher_query_action():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)

    dispatchers = action_mapper._build_dispatcher()

    assert hasattr(dispatchers[ActionType.QUERY]["validator"], "validate")
    assert dispatchers[ActionType.QUERY]["action"] == expected_actions.query


def test_build_dispatcher_commit_changes_action():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)

    dispatchers = action_mapper._build_dispatcher()

    assert (
        dispatchers[ActionType.COMMIT_CHANGES]["action"]
        == expected_actions.commit_changes
    )
    assert dispatchers[ActionType.COMMIT_CHANGES]["validator"] is None


def test_unknown_action_dispatcher():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)
    unknown_action = "UNKNOWN_ACTION"

    with pytest.raises(UnknownActionDispatcher) as exc_info:
        action_mapper.get_action_dispatcher(unknown_action)

    expected_error_message = f"Exception at dispatch: action {unknown_action} unknown"
    assert re.search(re.escape(expected_error_message), str(exc_info.value)) is not None
