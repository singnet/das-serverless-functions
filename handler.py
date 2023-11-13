import json
import base64
import time
from config import load_env
from validators.event import EventValidator
from actions import Actions, ActionType
from validators import validate
from validators.actions import (
    NodeExistsValidator,
    LinkExistsValidator,
    GetNodeHandleValidator,
    GetLinkHandleValidator,
    GetLinkTargetsValidator,
    IsOrderedValidator,
    GetMatchedLinksValidator,
    GetAllNodeValidator,
    GetMatchedTypeTemplateValidator,
    GetMatchedTypeValidator,
    GetNodeNameValidator,
    GetMatchedNodeNameValidator,
    GetAtomAsDictValidator,
    GetAtomAsDeepRepresentationValidator,
    GetLinkTypeValidator,
    GetNodeTypeValidator,
)
from hyperon_das_atomdb.exceptions import (
    NodeDoesNotExistException,
    LinkDoesNotExistException,
)

load_env()


def _get_payload(event: any):
    if isinstance(event, str):  # vultr
        return json.loads(event)

    body = event.get("body", event)

    if isinstance(body, str):
        return json.loads(base64.b64decode(body))  # aws

    return event


def handle(event: any, context=None):
    # start = time.time()

    payload = validate(EventValidator(), _get_payload(event))
    result = None
    actions = Actions()
    http_code_response = 200

    if payload["action"] == ActionType.NODE_EXISTS:
        node_exists_payload = validate(
            NodeExistsValidator(),
            payload["input"],
        )
        try:
            result = actions.node_exists(
                node_exists_payload["node_type"],
                node_exists_payload["node_name"],
            )
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.LINK_EXISTS:
        link_exists_payload = validate(
            LinkExistsValidator(),
            payload["input"],
        )
        try:
            result = actions.link_exists(
                link_exists_payload["link_type"],
                link_exists_payload["target_handles"],
            )
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.GET_NODE_HANDLE:
        get_node_handle_payload = validate(
            GetNodeHandleValidator(),
            payload["input"],
        )
        try:
            result = actions.get_node_handle(
                get_node_handle_payload["node_type"],
                get_node_handle_payload["node_name"],
            )
        except NodeDoesNotExistException as e:
            result = dict(error=e.message)
            http_code_response = 404
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.GET_LINK_HANDLE:
        get_link_handle_payload = validate(
            GetLinkHandleValidator(),
            payload["input"],
        )
        try:
            result = actions.get_link_handle(
                get_link_handle_payload["link_type"],
                get_link_handle_payload["target_handles"],
            )
        except LinkDoesNotExistException as e:
            result = dict(error=e.message)
            http_code_response = 404
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.GET_LINK_TARGETS:
        get_link_targets_payload = validate(
            GetLinkTargetsValidator(),
            payload["input"],
        )
        try:
            result = actions.get_link_targets(get_link_targets_payload["link_handle"])
        except ValueError as e:
            result = dict(error=e.message)
            http_code_response = 400
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.IS_ORDERED:
        is_ordered_payload = validate(
            IsOrderedValidator(),
            payload["input"],
        )
        try:
            result = actions.is_ordered(is_ordered_payload["link_handle"])
        except ValueError as e:
            result = dict(error=e.message)
            http_code_response = 400
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.GET_MATCHED_LINKS:
        get_matched_links_payload = validate(
            GetMatchedLinksValidator(),
            payload["input"],
        )
        result = actions.get_matched_links(
            get_matched_links_payload["link_type"],
            get_matched_links_payload["target_handles"],
            payload["input"].get("extra_parameters"),
        )
    elif payload["action"] == ActionType.GET_ALL_NODES:
        get_all_nodes_payload = validate(
            GetAllNodeValidator(),
            payload["input"],
        )
        try:
            result = actions.get_all_nodes(
                get_all_nodes_payload["node_type"],
                get_all_nodes_payload["names"],
            )
        except ValueError as e:
            result = dict(error=e.message)
            http_code_response = 400
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.GET_MATCHED_TYPE_TEMPLATE:
        get_matched_type_template_payload = validate(
            GetMatchedTypeTemplateValidator(),
            payload["input"],
        )
        try:
            result = actions.get_matched_type_template(
                get_matched_type_template_payload["template"],
                payload["input"].get("extra_parameters"),
            )
        except ValueError as e:
            result = dict(error=e.message)
            http_code_response = 400
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.GET_MATCHED_TYPE:
        get_matched_type_payload = validate(
            GetMatchedTypeValidator(),
            payload["input"],
        )
        try:
            result = actions.get_matched_type(
                get_matched_type_payload["link_type"],
                payload["input"].get("extra_parameters"),
            )
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.GET_NODE_NAME:
        get_node_name_payload = validate(
            GetNodeNameValidator(),
            payload["input"],
        )
        try:
            result = actions.get_node_name(get_node_name_payload["node_handle"])
        except ValueError as e:
            result = dict(error=e.message)
            http_code_response = 400
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.GET_MATCHED_NODE_NAME:
        get_matched_node_name_payload = validate(
            GetMatchedNodeNameValidator(),
            payload["input"],
        )
        try:
            result = actions.get_matched_node_name(
                get_matched_node_name_payload["node_type"],
                get_matched_node_name_payload["substring"],
            )
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.GET_ATOM_AS_DICT:
        get_atom_as_dict_payload = validate(
            GetAtomAsDictValidator(),
            payload["input"],
        )
        try:
            result = actions.get_atom_as_dict(
                get_atom_as_dict_payload["handle"],
                get_atom_as_dict_payload["arity"],
            )
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.GET_ATOM_AS_DEEP_REPRESENTATION:
        get_atom_as_deep_representation_payload = validate(
            GetAtomAsDeepRepresentationValidator(),
            payload["input"],
        )
        try:
            result = actions.get_atom_as_deep_representation(
                get_atom_as_deep_representation_payload["handle"],
                get_atom_as_deep_representation_payload["arity"],
            )
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.GET_LINK_TYPE:
        get_link_type_payload = validate(
            GetLinkTypeValidator(),
            payload["input"],
        )
        try:
            result = actions.get_link_type(get_link_type_payload["link_handle"])
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.GET_NODE_TYPE:
        get_node_type_payload = validate(
            GetNodeTypeValidator(),
            payload["input"],
        )
        try:
            result = actions.get_node_type(get_node_type_payload["node_handle"])
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.COUNT_ATOMS:
        try:
            result = actions.count_atoms()
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.CLEAR_DATABASE:
        try:
            result = actions.clear_database()
        except Exception as e:
            result = dict(error=e.message)
            http_code_response = 500
    elif payload["action"] == ActionType.PING:
        result = dict(message="pong")
    else:
        result = dict(error=f'The action {payload["action"]} was not found')
        http_code_response = 400

    # end = time.time()
    # total = end - start

    # data = {
    #     "result": result,
    #     "timestamp": total,
    # }

    return (
        result
        if context is None
        else (
            context.status(http_code_response)
            .headers({"Content-Type": "application/json"})
            .success(result)
        )
    )
