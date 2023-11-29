import json
import base64
from utils import load_env, logger, LogicalExpressionParser
from validators.event import EventValidator
from actions import Actions, ActionType
from validators import validate
from validators.actions import (
    GetAtomValidator,
    GetNodeValidator,
    GetNodesValidator,
    GetLinkValidator,
    GetLinksValidator,
    GetLinkTypeValidator,
    GetLinkTargetsValidator,
    GetNodeTypeValidator,
    QueryValidator,
    PatternMatcherQueryValidator,
    GetNodeNameValidator,
)


load_env()


def _response(http_code_response: int, result: str, context: any = None):
    logger().info(f"Function response ({http_code_response}): {result}")

    if context is None:
        try:
            return json.loads(result)
        except:
            return result

    return {
        "statusCode": http_code_response,
        "body": json.dumps(result),
        "headers": {"Content-Type": "application/json"},
    }


def _get_payload(event: any):
    if isinstance(event, str):  # vultr
        logger().info(f"Received Vultr source payload: {event}")
        return json.loads(event)

    body = event.get("body", event)  # aws

    if isinstance(body, str):
        if event.get("isBase64Encoded") is True:
            logger().info(f"Received AWS source payload (Base64 encoded): {body}")
            return json.loads(base64.b64decode(body))

        logger().info(f"Received AWS source payload: {body}")
        return json.loads(body)

    logger().info(f"Received unknown payload source: {event}")
    return body


def handle(event: any, context=None):
    payload = validate(EventValidator(), _get_payload(event))
    result = None
    actions = None
    http_code_response = 200

    try:
        actions = Actions()
    except Exception as e:
        logger().error(f"Exception caught at Actions instance: {str(e)}")
        result = dict(error=str(e))
        http_code_response = 400
        return _response(http_code_response, result, context)

    try:
        if payload["action"] == ActionType.PING:
            result = dict(message="pong")
        elif payload["action"] == ActionType.CLEAR_DATABASE:
            result = actions.clear_database()
        elif payload["action"] == ActionType.COUNT_ATOMS:
            result = actions.count_atoms()
        elif payload["action"] == ActionType.GET_ATOM:
            get_atom_payload = validate(
                GetAtomValidator(),
                payload["input"],
            )
            result = actions.get_atom(
                handle=get_atom_payload["handle"],
                output_format=get_atom_payload.get("output_format", None),
            )
        elif payload["action"] == ActionType.GET_NODE:
            get_node_payload = validate(
                GetNodeValidator(),
                payload["input"],
            )
            result = actions.get_node(
                node_type=get_node_payload["node_type"],
                node_name=get_node_payload["node_name"],
                output_format=get_node_payload.get("output_format", None),
            )

        elif payload["action"] == ActionType.GET_NODES:
            get_nodes_payload = validate(
                GetNodesValidator(),
                payload["input"],
            )
            result = actions.get_nodes(
                node_type=get_nodes_payload["node_type"],
                node_name=get_nodes_payload["node_name"],
                output_format=get_nodes_payload.get("output_format", None),
            )
        elif payload["action"] == ActionType.GET_LINK:
            get_link_payload = validate(
                GetLinkValidator(),
                payload["input"],
            )
            result = actions.get_link(
                link_type=get_link_payload["link_type"],
                targets=get_link_payload["targets"],
                output_format=get_link_payload.get("output_format", None),
            )
        elif payload["action"] == ActionType.GET_LINKS:
            get_links_payload = validate(
                GetLinksValidator(),
                payload["input"],
            )
            result = actions.get_links(
                link_type=get_links_payload["link_type"],
                target_types=get_links_payload.get("target_types", None),
                targets=get_links_payload.get("targets", None),
                output_format=get_links_payload.get("output_format", None),
            )
        elif payload["action"] == ActionType.GET_LINK_TYPE:
            get_link_type_payload = validate(
                GetLinkTypeValidator(),
                payload["input"],
            )
            result = actions.get_link_type(
                link_handle=get_link_type_payload["link_handle"],
            )
        elif payload["action"] == ActionType.GET_LINK_TARGETS:
            get_link_targets_payload = validate(
                GetLinkTargetsValidator(),
                payload["input"],
            )
            result = actions.get_link_targets(
                link_handle=get_link_targets_payload["link_handle"],
            )
        elif payload["action"] == ActionType.GET_NODE_TYPE:
            get_node_type_payload = validate(
                GetNodeTypeValidator(),
                payload["input"],
            )
            result = actions.get_node_type(
                node_handle=get_node_type_payload["node_handle"],
            )
        elif payload["action"] == ActionType.GET_NODE_NAME:
            get_node_name_payload = validate(
                GetNodeNameValidator(),
                payload["input"],
            )
            result = actions.get_node_name(
                node_handle=get_node_name_payload["node_handle"],
            )
        elif payload["action"] == ActionType.QUERY:
            query_payload = validate(
                QueryValidator(),
                payload["input"],
            )
            result = actions.query(
                query=query_payload["query"],
                extra_parameters=query_payload.get("extra_parameters", None),
            )
        elif payload["action"] == ActionType.PATTERN_MATCHER_QUERY:
            pattern_matcher_query_payload = validate(
                PatternMatcherQueryValidator(),
                payload["input"],
            )
            logical_expression_parser = LogicalExpressionParser()
            query = logical_expression_parser.from_dict(
                pattern_matcher_query_payload["query"]
            )

            pattern_matcher_query_payload["query"] = query

            result = actions.pattern_matcher_query(
                query=pattern_matcher_query_payload["query"],
                extra_parameters=pattern_matcher_query_payload.get(
                    "extra_parameters", None
                ),
            )
    except Exception as e:
        logger().error(f"Exception caught at action {payload['action']}: {str(e)}")
        result = dict(error=str(e))
        http_code_response = 500

    return _response(http_code_response, result, context)
