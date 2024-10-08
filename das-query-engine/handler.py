import traceback
from typing import Any

from action_dispatcher import ActionDispatcher
from action_mapper import ActionMapper
from exceptions import Conflict, PayloadMalformed, UnknownActionDispatcher, UnreachableConnection
from hyperon_das.logger import logger
from utils.dotenv import load_env
from validators import validate
from validators.event import EventValidator


def _response(
    http_code_response: int,
    result: Any,
    headers: dict = {},
):
    logger().info(f"Function status code response - {http_code_response}")

    return {
        "statusCode": http_code_response,
        "body": result,
        "headers": headers,
    }


# TODO: refactor status code comes from actions now and the handler only returns it to the client
def handle(event: Any, context=None):
    load_env()

    result = None
    http_code_response = None
    elapsed_time = None

    try:
        payload = validate(EventValidator(), event.get("body", {}))

        action_dispatcher = ActionDispatcher(action_mapper=ActionMapper())

        result, http_code_response, elapsed_time = action_dispatcher.dispatch(
            action_type=payload["action"],
            payload=payload["input"],
        )

    except PayloadMalformed as e:
        trace = traceback.format_exc()
        error_message = f"{str(e)}\n{trace}"
        logger().error(error_message)
        result = dict(error=error_message)
        http_code_response = 400
    except UnknownActionDispatcher as e:
        trace = traceback.format_exc()
        error_message = f"{str(e)}\n{trace}"
        logger().error(error_message)
        result = dict(error=error_message)
        http_code_response = 404
    except Conflict as e:
        trace = traceback.format_exc()
        error_message = f"{str(e)}\n{trace}"
        logger().error(error_message)
        result = dict(error=error_message)
        http_code_response = 409
    except Exception as e:
        trace = traceback.format_exc()
        error_message = f"{str(e)}\n{trace}"
        logger().error(error_message)
        result = dict(error=error_message)
        http_code_response = 500

    return _response(
        http_code_response,
        result,
        headers={
            "X-Handler-Method-Timestamp": elapsed_time,
        },
    )
