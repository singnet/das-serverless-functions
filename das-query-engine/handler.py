import base64
import json
import traceback

from action_dispatcher import ActionDispatcher
from action_mapper import ActionMapper
from exceptions import PayloadMalformed, UnknownActionDispatcher, UnreachableConnection
from hyperon_das.logger import logger
from utils.dotenv import load_env
from validators import validate
from validators.event import EventValidator

load_env()


def _response(
    http_code_response: int,
    result: str,
    headers: dict = {},
):
    logger().info(f"Function status code response - {http_code_response}")

    return {
        "statusCode": http_code_response,
        "body": json.dumps(result, default=str, indent=4),
        "headers": {
            "Content-Type": "application/json",
            "X-Handler-Method-Timestamp": headers.get("X-Handler-Method-Timestamp", None),
        },
    }


def _get_payload(event: any):
    body = event.get("body", event)

    if isinstance(body, str):  # aws
        if event.get("isBase64Encoded") is True:
            logger().info(f"Received AWS source payload (Base64 encoded): {body}")
            return json.loads(base64.b64decode(body))

        logger().info(f"Received AWS source payload: {body}")
        return json.loads(body)

    logger().info(f"Received Vultr payload source: {event}")
    return body  # vultr


def handle(event: any, context=None):
    result = None
    http_code_response = 200
    elapsed_time = None

    try:
        payload = validate(EventValidator(), _get_payload(event))

        action_dispatcher = ActionDispatcher(action_mapper=ActionMapper())

        result, elapsed_time = action_dispatcher.dispatch(
            action_type=payload["action"],
            payload=payload["input"],
        )

    except PayloadMalformed as e:
        trace = traceback.format_exc()
        logger().error(f"{str(e)}\n{trace}")
        result = dict(error=str(e))
        http_code_response = 400
    except UnknownActionDispatcher as e:
        trace = traceback.format_exc()
        logger().error(f"{str(e)}\n{trace}")
        result = dict(error=str(e))
        http_code_response = 404
    except (Exception, UnreachableConnection) as e:
        trace = traceback.format_exc()
        logger().error(f"{str(e)}\n{trace}")
        result = dict(error=str(e))
        http_code_response = 500

    return _response(
        http_code_response,
        result,
        headers={
            "X-Handler-Method-Timestamp": elapsed_time,
        },
    )
