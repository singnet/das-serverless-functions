import json
from .config import load_env
from .exceptions import UnknownEventAction
from .actions import ActionType
from .validators.event import EventValidator
from .actions.actions import (
    node_exists,
    link_exists,
    get_node_handle,
    get_link_handle,
    get_link_targets,
    is_ordered,
    get_matched_links,
    get_all_nodes,
    get_matched_type_template,
    get_matched_type,
    get_node_name,
    get_matched_node_name,
    get_atom_as_dict,
    get_atom_as_deep_representation,
    get_link_type,
    get_node_type,
    count_atoms,
    clear_database,
)
from .validators import validate
from .validators.actions import (
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


load_env()


def handle(event: str, context=None):
    payload = validate(EventValidator, json.loads(event))
    result = None

    if payload.action == ActionType.NODE_EXISTS:
        node_exists_payload = validate(
            NodeExistsValidator,
            payload.input,
        )
        result = node_exists(
            node_exists_payload.node_type,
            node_exists_payload.node_name,
        )
    elif payload.action == ActionType.LINK_EXISTS:
        link_exists_payload = validate(
            LinkExistsValidator,
            payload.input,
        )
        result = link_exists(
            link_exists_payload.link_type,
            link_exists_payload.target_handles,
        )
    elif payload.action == ActionType.GET_NODE_HANDLE:
        get_node_handle_payload = validate(
            GetNodeHandleValidator,
            payload.input,
        )
        result = get_node_handle(
            get_node_handle_payload.node_type,
            get_node_handle_payload.node_name,
        )
    elif payload.action == ActionType.GET_LINK_HANDLE:
        get_link_handle_payload = validate(GetLinkHandleValidator)
        result = get_link_handle(
            get_link_handle_payload.link_type,
            get_link_handle_payload.target_handles,
        )
    elif payload.action == ActionType.GET_LINK_TARGETS:
        get_link_targets_payload = validate(
            GetLinkTargetsValidator,
            payload.input,
        )
        result = get_link_targets(get_link_targets_payload.link_handle)
    elif payload.action == ActionType.IS_ORDERED:
        is_ordered_payload = validate(
            IsOrderedValidator,
            payload.input,
        )
        result = is_ordered(is_ordered_payload.link_handle)
    elif payload.action == ActionType.GET_MATCHED_LINKS:
        get_matched_links_payload = validate(
            GetMatchedLinksValidator,
            payload.input,
        )
        result = get_matched_links(
            get_matched_links_payload.link_type,
            get_matched_links_payload.target_handles,
            get_matched_links_payload.extra_parameters,
        )
    elif payload.action == ActionType.GET_ALL_NODES:
        get_all_nodes_payload = validate(
            GetAllNodeValidator,
            payload.input,
        )
        result = get_all_nodes(
            get_all_nodes_payload.link_type,
            get_all_nodes_payload.names,
        )
    elif payload.action == ActionType.GET_MATCHED_TYPE_TEMPLATE:
        get_matched_type_template_payload = validate(
            GetMatchedTypeTemplateValidator,
            payload.input,
        )
        result = get_matched_type_template(
            get_matched_type_template_payload.template,
            get_matched_type_template_payload.extra_parameters,
        )
    elif payload.action == ActionType.GET_MATCHED_TYPE:
        get_matched_type_payload = validate(
            GetMatchedTypeValidator,
            payload.input,
        )
        result = get_matched_type(
            get_matched_type_payload.link_type,
            get_matched_type_payload.extra_parameters,
        )
    elif payload.action == ActionType.GET_NODE_NAME:
        get_node_name_payload = validate(
            GetNodeNameValidator,
            payload.input,
        )
        result = get_node_name(get_node_name_payload.node_handle)
    elif payload.action == ActionType.GET_MATCHED_NODE_NAME:
        get_matched_node_name_payload = validate(
            GetMatchedNodeNameValidator,
            payload.input,
        )
        result = get_matched_node_name(
            get_matched_node_name_payload.node_type,
            get_matched_node_name_payload.substring,
        )
    elif payload.action == ActionType.GET_ATOM_AS_DICT:
        get_atom_as_dict_payload = validate(
            GetAtomAsDictValidator,
            payload.input,
        )
        result = get_atom_as_dict(
            get_atom_as_dict_payload.handle,
            get_atom_as_dict_payload.arity,
        )
    elif payload.action == ActionType.GET_ATOM_AS_DEEP_REPRESENTATION:
        get_atom_as_deep_representation_payload = get_atom_as_deep_representation(
            GetAtomAsDeepRepresentationValidator, payload.input
        )
        result = get_atom_as_deep_representation(
            get_atom_as_deep_representation_payload.handle,
            get_atom_as_deep_representation_payload.arity,
        )
    elif payload.action == ActionType.GET_LINK_TYPE:
        get_link_type_payload = validate(
            GetLinkTypeValidator,
            payload.input,
        )
        result = get_link_type(get_link_type_payload.link_handle)
    elif payload.action == ActionType.GET_NODE_TYPE:
        get_node_type_payload = validate(
            GetNodeTypeValidator,
            payload.input,
        )
        result = get_node_type(get_node_type_payload.node_handle)
    elif payload.action == ActionType.COUNT_ATOMS:
        result = count_atoms()
    elif payload.action == ActionType.CLEAR_DATABASE:
        result = clear_database()
    elif payload.action == ActionType.PING:
        result = {"message": "pong"}
    else:
        raise UnknownEventAction()

    return (
        result
        if context is None
        else (
            context.status(200)
            .headers({"Content-Type": "application/json"})
            .success(result)
        )
    )
