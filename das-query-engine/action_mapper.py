from typing import Any, Dict

from actions import Actions, ActionType
from exceptions import UnknownActionDispatcher
from validators.actions import (
    CommitChangesValidator,
    CreateContextValidator,
    CreateFieldIndexValidator,
    CustomQueryValidator,
    FetchValidator,
    GetAtomsByField,
    GetAtomsByTextField,
    GetAtomValidator,
    GetIncomingLinksValidator,
    GetLinksValidator,
    GetLinkValidator,
    GetNodeByNameStartingWith,
    GetNodeValidator,
    HandshakeValidator,
    QueryValidator,
    CountAtomsValidator
)


class ActionMapper:
    def _get_actions(self) -> Actions:
        return Actions()

    def _build_dispatcher(self):
        actions = self._get_actions()

        return {
            ActionType.PING: {
                "action": actions.ping,
                "validator": None,
            },
            ActionType.HANDSHAKE: {
                "action": actions.handshake,
                "validator": HandshakeValidator,
            },
            ActionType.COUNT_ATOMS: {
                "action": actions.count_atoms,
                "validator": CountAtomsValidator,
            },
            ActionType.GET_ATOM: {
                "action": actions.get_atom,
                "validator": GetAtomValidator,
            },
            ActionType.GET_NODE: {
                "action": actions.get_node,
                "validator": GetNodeValidator,
            },
            ActionType.GET_LINK: {
                "action": actions.get_link,
                "validator": GetLinkValidator,
            },
            ActionType.GET_LINKS: {
                "action": actions.get_links,
                "validator": GetLinksValidator,
            },
            ActionType.QUERY: {
                "action": actions.query,
                "validator": QueryValidator,
            },
            ActionType.COMMIT_CHANGES: {
                "action": actions.commit_changes,
                "validator": CommitChangesValidator,
            },
            ActionType.GET_INCOMING_LINKS: {
                "action": actions.get_incoming_links,
                "validator": GetIncomingLinksValidator,
            },
            ActionType.CREATE_FIELD_INDEX: {
                "action": actions.create_field_index,
                "validator": CreateFieldIndexValidator,
            },
            ActionType.CUSTOM_QUERY: {
                "action": actions.custom_query,
                "validator": CustomQueryValidator,
            },
            ActionType.FETCH: {
                "action": actions.fetch,
                "validator": FetchValidator,
            },
            ActionType.CREATE_CONTEXT: {
                "action": actions.create_context,
                "validator": CreateContextValidator,
            },
            ActionType.GET_ATOMS_BY_FIELD: {
                "action": actions.get_atoms_by_field,
                "validator": GetAtomsByField,
            },
            ActionType.GET_ATOMS_BY_TEXT_FIELD: {
                "action": actions.get_atoms_by_text_field,
                "validator": GetAtomsByTextField,
            },
            ActionType.GET_NODE_BY_NAME_STARTING_WITH: {
                "action": actions.get_node_by_name_starting_with,
                "validator": GetNodeByNameStartingWith,
            },
        }

    def get_action_dispatcher(self, action_type: ActionType) -> Dict[str, Any]:
        action_map = self._build_dispatcher().get(action_type)

        if action_map is None:
            raise UnknownActionDispatcher(f"Exception at dispatch: action {action_type} unknown")
        return action_map
