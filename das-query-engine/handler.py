import json
import base64
from utils import load_env, LogicalExpressionParser
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
)


load_env()


def _response(http_code_response, result, context):
    if context is None:
        return result

    return {
        "statusCode": http_code_response,
        "body": json.dumps(result),
        "headers": {"Content-Type": "application/json"},
    }


def _get_payload(event: any):
    if isinstance(event, str):  # vultr
        return json.loads(event)

    body = event.get("body", event)  # aws

    if isinstance(body, str):
        if event.get("isBase64Encoded") is True:
            return json.loads(base64.b64decode(body))

        return json.loads(body)

    return body


def handle(event: any, context=None):
    payload = validate(EventValidator(), _get_payload(event))
    result = None
    actions = None
    http_code_response = 200

    try:
        actions = Actions()
    except Exception as e:
        result = dict(error=str(e))
        http_code_response = 400
        return _response(http_code_response, result, context)

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
        try:
            result = actions.get_atom(
                handle=get_atom_payload["handle"],
                output_format=get_atom_payload.get("output_format"),
            )
        except Exception as e:
            result = dict(error=str(e))
            http_code_response = 500
    elif payload["action"] == ActionType.GET_NODE:
        get_node_payload = validate(
            GetNodeValidator(),
            payload["input"],
        )
        try:
            result = actions.get_node(
                node_type=get_node_payload["node_type"],
                node_name=get_node_payload["node_name"],
                output_format=get_node_payload.get("output_format"),
            )
        except Exception as e:
            result = dict(error=str(e))
            http_code_response = 500
    elif payload["action"] == ActionType.GET_NODES:
        get_nodes_payload = validate(
            GetNodesValidator(),
            payload["input"],
        )
        try:
            result = actions.get_nodes(
                node_type=get_nodes_payload["node_type"],
                node_name=get_nodes_payload["node_name"],
                output_format=get_nodes_payload.get("output_format"),
            )
        except Exception as e:
            result = dict(error=str(e))
            http_code_response = 500
    elif payload["action"] == ActionType.GET_LINK:
        get_link_payload = validate(
            GetLinkValidator(),
            payload["input"],
        )
        try:
            result = actions.get_link(
                link_type=get_link_payload["link_type"],
                targets=get_link_payload.get("targets"),
                output_format=get_link_payload.get("output_format"),
            )
        except Exception as e:
            result = dict(error=str(e))
            http_code_response = 500
    elif payload["action"] == ActionType.GET_LINKS:
        get_links_payload = validate(
            GetLinksValidator(),
            payload["input"],
        )
        try:
            result = actions.get_links(
                link_type=get_links_payload["link_type"],
                target_types=get_links_payload.get("target_types"),
                targets=get_links_payload.get("targets"),
                output_format=get_links_payload.get("output_format"),
            )
        except Exception as e:
            result = dict(error=str(e))
            http_code_response = 500
    elif payload["action"] == ActionType.GET_LINK_TYPE:
        get_link_type_payload = validate(
            GetLinkTypeValidator(),
            payload["input"],
        )
        try:
            result = actions.get_link_type(
                link_handle=get_link_type_payload["link_handle"],
            )
        except Exception as e:
            result = dict(error=str(e))
            http_code_response = 500
    elif payload["action"] == ActionType.GET_LINK_TARGETS:
        get_link_targets_payload = validate(
            GetLinkTargetsValidator(),
            payload["input"],
        )
        try:
            result = actions.get_link_targets(
                link_handle=get_link_targets_payload["link_handle"],
            )
        except Exception as e:
            result = dict(error=str(e))
            http_code_response = 500
    elif payload["action"] == ActionType.GET_NODE_TYPE:
        get_node_type_payload = validate(
            GetNodeTypeValidator(),
            payload["input"],
        )
        try:
            result = actions.get_node_type(
                node_handle=get_node_type_payload["node_handle"],
            )
        except Exception as e:
            result = dict(error=str(e))
            http_code_response = 500
    elif payload["action"] == ActionType.GET_NODE_NAME:
        get_node_name_payload = validate(
            GetNodeTypeValidator(),
            payload["input"],
        )
        try:
            result = actions.get_node_name(
                node_handle=get_node_name_payload["node_handle"],
            )
        except Exception as e:
            result = dict(error=str(e))
            http_code_response = 500
    elif payload["action"] == ActionType.QUERY:
        query_payload = validate(
            QueryValidator(),
            payload["input"],
        )
        try:
            result = actions.query(
                query=query_payload["query"],
                extra_parameters=query_payload.get("extra_parameters"),
            )
        except Exception as e:
            result = dict(error=str(e))
            http_code_response = 500
    elif payload["action"] == ActionType.PATTERN_MATCHER_QUERY:
        pattern_matcher_query_payload = validate(
            PatternMatcherQueryValidator(),
            payload["input"],
        )
        try:
            logical_expression_parser = LogicalExpressionParser()
            query = logical_expression_parser.from_dict(
                pattern_matcher_query_payload["query"]
            )

            pattern_matcher_query_payload["query"] = query

            result = actions.pattern_matcher_query(
                query=pattern_matcher_query_payload["query"],
                extra_parameters=pattern_matcher_query_payload.get("extra_parameters"),
            )
        except Exception as e:
            result = dict(error=str(e))
            http_code_response = 500

    return _response(http_code_response, result, context)
