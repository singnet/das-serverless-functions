from enum import Enum
from hyperon_das.api import DistributedAtomSpace, QueryOutputFormat, LogicalExpression
from typing import List, Dict, Any, Tuple
from utils import remove_none_args


class ActionType(str, Enum):
    CLEAR_DATABASE = "clear_database"
    COUNT_ATOMS = "count_atoms"
    GET_ATOM = "get_atom"
    GET_NODE = "get_node"
    GET_NODES = "get_nodes"
    GET_LINK = "get_link"
    GET_LINKS = "get_links"
    GET_LINK_TYPE = "get_link_type"
    GET_LINK_TARGETS = "get_link_targets"
    GET_NODE_TYPE = "get_node_type"
    GET_NODE_NAME = "get_node_name"
    QUERY = "query"
    PATTERN_MATCHER_QUERY = "pattern_matcher_query"
    ADD_NODE = "add_node"
    ADD_LINK = "add_link"
    PING = "ping"


class Actions:
    def __init__(self) -> None:
        self.distributed_atom_space = DistributedAtomSpace("server")

    def ping(self) -> dict:
        return dict(message="pong")

    def clear_database(self) -> None:
        return self.distributed_atom_space.clear_database()

    def count_atoms(self) -> Tuple[int, int]:
        return self.distributed_atom_space.count_atoms()

    @remove_none_args
    def get_atom(
        self,
        handle: str,
        output_format: str = "HANDLE",
    ) -> str | dict:
        output_format_enum = getattr(
            QueryOutputFormat,
            output_format.upper(),
            QueryOutputFormat.HANDLE,
        )
        return self.distributed_atom_space.get_atom(handle, output_format_enum)

    @remove_none_args
    def get_node(
        self,
        node_type: str,
        node_name: str,
        output_format: str = "HANDLE",
    ) -> str | dict:
        output_format_enum = getattr(
            QueryOutputFormat,
            output_format.upper(),
            QueryOutputFormat.HANDLE,
        )

        return self.distributed_atom_space.get_node(
            node_type,
            node_name,
            output_format_enum,
        )

    @remove_none_args
    def get_nodes(
        self,
        node_type: str,
        node_name: str = None,
        output_format: str = "HANDLE",
    ) -> List[str] | List[Dict]:
        output_format_enum = getattr(
            QueryOutputFormat,
            output_format.upper(),
            QueryOutputFormat.HANDLE,
        )

        return self.distributed_atom_space.get_nodes(
            node_type,
            node_name,
            output_format_enum,
        )

    @remove_none_args
    def get_link(
        self,
        link_type: str,
        targets: List[str],
        output_format: str = "HANDLE",
    ) -> str | Dict:
        output_format_enum = getattr(
            QueryOutputFormat,
            output_format.upper(),
            QueryOutputFormat.HANDLE,
        )

        return self.distributed_atom_space.get_link(
            link_type,
            targets,
            output_format_enum,
        )

    @remove_none_args
    def get_links(
        self,
        link_type: str,
        target_types: str = None,
        targets: List[str] = None,
        output_format: str = "HANDLE",
    ) -> List[str] | List[Dict]:
        output_format_enum = getattr(
            QueryOutputFormat,
            output_format.upper(),
            QueryOutputFormat.HANDLE,
        )

        return self.distributed_atom_space.get_links(
            link_type,
            target_types,
            targets,
            output_format_enum,
        )

    def get_link_type(self, link_handle: str) -> str:
        return self.distributed_atom_space.get_link_type(link_handle)

    def get_link_targets(
        self,
        link_handle: str,
    ) -> List[str]:
        return self.distributed_atom_space.get_link_targets(link_handle)

    def get_node_type(self, node_handle: str) -> str:
        return self.distributed_atom_space.get_node_type(node_handle)

    def get_node_name(self, node_handle: str) -> str:
        return self.distributed_atom_space.get_node_name(node_handle)

    @remove_none_args
    def query(
        self,
        query: Dict[str, Any],
        extra_parameters: Dict[str, Any] | None = None,
    ) -> List[Dict[str, Any]]:
        return self.distributed_atom_space.query(query, extra_parameters)

    @remove_none_args
    def pattern_matcher_query(
        self,
        query: LogicalExpression,
        extra_parameters: Dict[str, Any] | None = None,
    ) -> dict | list | None:
        return self.distributed_atom_space.pattern_matcher_query(
            query, extra_parameters
        )
