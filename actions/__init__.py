from enum import Enum


class ActionType(Enum):
    NODE_EXISTS = "node_exists"
    LINK_EXISTS = "link_exists"
    GET_NODE_HANDLE = "get_node_handle"
    GET_LINK_HANDLE = "get_link_handle"
    GET_LINK_TARGETS = "get_link_targets"
    IS_ORDERED = "is_ordered"
    GET_MATCHED_LINKS = "get_matched_links"
    GET_ALL_NODES = "get_all_nodes"
    GET_MATCHED_TYPE_TEMPLATE = "get_matched_type_template"
    GET_MATCHED_TYPE = "get_matched_type"
    GET_NODE_NAME = "get_node_name"
    GET_MATCHED_NODE_NAME = "get_matched_node_name"
    GET_ATOM_AS_DICT = "get_atom_as_dict"
    GET_ATOM_AS_DEEP_REPRESENTATION = "get_atom_as_deep_representation"
    GET_LINK_TYPE = "get_link_type"
    GET_NODE_TYPE = "get_node_type"
    COUNT_ATOMS = "count_atoms"
    CLEAR_DATABASE = "clear_database"
