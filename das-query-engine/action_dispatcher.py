from typing import Union
from actions import ActionType, Actions
from validators.actions import (
    GetAtomValidator,
    GetNodeValidator,
    GetLinkValidator,
    GetLinksValidator,
    QueryValidator,
)
from exceptions import UnknownActionDispatcher, PayloadMalformed
from validators import validate


class ActionDispatcher:
    def __init__(self) -> None:
        actions = Actions()

        self._map_dispatcher = {
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
        }

    def dispatch(
        self,
        action_type: ActionType,
        payload: dict = {},
    ) -> Union[tuple, None]:
        action_map = self._map_dispatcher.get(action_type, None)

        if action_map is None:
            raise UnknownActionDispatcher(
                f"Exception at dispatch: action {action_type} unknown"
            )

        action = action_map["action"]
        validator = action_map.get("validator", None)

        if validator is not None:
            try:
                payload = validate(
                    validator(),
                    payload,
                )

                return action(**payload)
            except PayloadMalformed as e:
                raise PayloadMalformed(
                    message=f"Exception at dispatch: payload malformed for action {action_type}",
                    details=str(e),
                )

        # When no validator is present, execute the action with an empty payload to prevent mass assignment in functions that do not accept these params.
        return action()
