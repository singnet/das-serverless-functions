from actions import Actions
from validators.actions import (
    GetAtomValidator,
    GetNodeValidator,
    GetLinkValidator,
    GetLinksValidator,
    QueryValidator,
    GetIncomingLinksValidator,
)
from actions import ActionType
from exceptions import UnknownActionDispatcher
from typing import Any, Dict


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
            ActionType.COUNT_ATOMS: {
                "action": actions.count_atoms,
                "validator": None,
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
                "validator": None,
            },
            ActionType.GET_INCOMING_LINKS: {
                "action": actions.get_incoming_links,
                "validator": GetIncomingLinksValidator,
            },
        }

    def get_action_dispatcher(self, action_type: ActionType) -> Dict[str, Any]:
        action_map = self._build_dispatcher().get(action_type)

        if action_map is None:
            raise UnknownActionDispatcher(
                f"Exception at dispatch: action {action_type} unknown"
            )
        return action_map
