import re
from unittest.mock import Mock

import pytest
from action_mapper import ActionMapper
from actions import ActionType
from exceptions import UnknownActionDispatcher


def test_build_dispatcher_handshake_action():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)

    dispatchers = action_mapper._build_dispatcher()

    assert isinstance(dispatchers, dict)
    assert dispatchers[ActionType.HANDSHAKE]["action"] == expected_actions.handshake
    assert dispatchers[ActionType.HANDSHAKE]["validator"] is None


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
    assert hasattr(dispatchers[ActionType.COUNT_ATOMS]["validator"], "validate")


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

    assert dispatchers[ActionType.COMMIT_CHANGES]["action"] == expected_actions.commit_changes
    assert hasattr(dispatchers[ActionType.COMMIT_CHANGES]["validator"], "validate")


def test_unknown_action_dispatcher():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)
    unknown_action = "UNKNOWN_ACTION"

    with pytest.raises(UnknownActionDispatcher) as exc_info:
        action_mapper.get_action_dispatcher(unknown_action)

    expected_error_message = f"Exception at dispatch: action {unknown_action} unknown"
    assert re.search(re.escape(expected_error_message), str(exc_info.value)) is not None


def test_build_dispatcher_fetch_action():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)

    dispatchers = action_mapper._build_dispatcher()

    assert hasattr(dispatchers[ActionType.FETCH]["validator"], "validate")
    assert dispatchers[ActionType.FETCH]["action"] == expected_actions.fetch


def test_build_dispatcher_custom_query_action():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)

    dispatchers = action_mapper._build_dispatcher()

    assert hasattr(dispatchers[ActionType.CUSTOM_QUERY]["validator"], "validate")
    assert dispatchers[ActionType.CUSTOM_QUERY]["action"] == expected_actions.custom_query


def test_build_dispatcher_get_atoms_by_field_action():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)

    dispatchers = action_mapper._build_dispatcher()

    assert hasattr(dispatchers[ActionType.GET_ATOMS_BY_FIELD]["validator"], "validate")
    assert (
        dispatchers[ActionType.GET_ATOMS_BY_FIELD]["action"] == expected_actions.get_atoms_by_field
    )


def test_build_dispatcher_get_atoms_by_text_field_action():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)

    dispatchers = action_mapper._build_dispatcher()

    assert hasattr(dispatchers[ActionType.GET_ATOMS_BY_TEXT_FIELD]["validator"], "validate")
    assert (
        dispatchers[ActionType.GET_ATOMS_BY_TEXT_FIELD]["action"]
        == expected_actions.get_atoms_by_text_field
    )


def test_build_dispatcher_get_node_by_name_starting_with_action():
    expected_actions = Mock()
    action_mapper = ActionMapper()
    action_mapper._get_actions = Mock(return_value=expected_actions)

    dispatchers = action_mapper._build_dispatcher()

    assert hasattr(dispatchers[ActionType.GET_NODE_BY_NAME_STARTING_WITH]["validator"], "validate")
    assert (
        dispatchers[ActionType.GET_NODE_BY_NAME_STARTING_WITH]["action"]
        == expected_actions.get_node_by_name_starting_with
    )
