from typing import Union
from actions import ActionType
from exceptions import UnknownActionDispatcher, PayloadMalformed
from validators import validate
from action_mapper import ActionMapper


class ActionDispatcher:
    def __init__(self, action_mapper: ActionMapper) -> None:
        self.action_mapper = action_mapper

    def dispatch(
        self,
        action_type: ActionType,
        payload: dict = {},
    ) -> Union[tuple, None]:
        action_map = self.action_mapper.get_action_dispatcher(action_type)

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
