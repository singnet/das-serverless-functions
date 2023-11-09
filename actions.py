import time
from enum import Enum
from function.das_atomdb.adapters import RedisMongoDB
from typing import Optional


class ActionType(str, Enum):
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
    PING = "ping"


class Actions:
    def __init__(self) -> None:
        start_time = time.time()
        self.redis_mongo_db = RedisMongoDB()
        end_time = time.time()
        print(f"MongoDB time: {end_time - start_time}")

    def node_exists(self, node_type: str, node_name: str) -> bool:
        return self.redis_mongo_db.node_exists(node_type, node_name)

    def link_exists(self, link_type: str, target_handles: list) -> bool:
        return self.redis_mongo_db.link_exists(link_type, target_handles)

    def get_node_handle(self, node_type: str, node_name: str) -> str:
        return self.redis_mongo_db.get_node_handle(node_type, node_name)

    def get_link_handle(self, link_type: str, target_handles: list) -> str:
        return self.redis_mongo_db.get_link_handle(link_type, target_handles)

    def get_link_targets(self, link_handle: str) -> list:
        return self.redis_mongo_db.get_link_targets(link_handle)

    def is_ordered(self, link_handle: str) -> bool:
        return self.redis_mongo_db.is_ordered(link_handle)

    def get_matched_links(
        self,
        link_type: str,
        target_handles: list,
        extra_parameters: Optional[dict] = None,
    ):
        return self.redis_mongo_db.get_matched_links(
            link_type, target_handles, extra_parameters
        )

    def get_all_nodes(self, node_type: str, names: bool = False) -> list:
        return self.redis_mongo_db.get_all_nodes(node_type, names)

    def get_matched_type_template(
        self,
        template: list,
        extra_parameters: Optional[dict] = None,
    ) -> list:
        return self.redis_mongo_db.get_matched_type_template(template, extra_parameters)

    def get_matched_type(
        self,
        link_type: str,
        extra_parameters: Optional[dict] = None,
    ) -> list:
        return self.redis_mongo_db.get_matched_type(link_type, extra_parameters)

    def get_node_name(self, node_handle: str) -> str:
        return self.redis_mongo_db.get_node_name(node_handle)

    def get_matched_node_name(self, node_type: str, substring: str) -> str:
        return self.redis_mongo_db.get_matched_node_name(node_type, substring)

    def get_atom_as_dict(self, handle, arity=-1) -> dict:
        return self.redis_mongo_db.get_atom_as_dict(handle, arity)

    def get_atom_as_deep_representation(
        self,
        handle: str,
        arity=-1,
    ) -> str:
        return self.redis_mongo_db.get_atom_as_deep_representation(handle, arity)

    def get_link_type(self, link_handle: str) -> str:
        return self.redis_mongo_db.get_link_type(link_handle)

    def get_node_type(self, node_handle: str) -> str:
        return self.redis_mongo_db.get_node_type(node_handle)

    def count_atoms(self) -> tuple([int, int]):
        return self.redis_mongo_db.count_atoms()

    def clear_database(self) -> None:
        return self.redis_mongo_db.clear_database()
