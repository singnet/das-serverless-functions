import os
from enum import Enum
from typing import Any, Dict, List, Tuple

from exceptions import UnreachableConnection
from hyperon_das import DistributedAtomSpace
from utils.decorators import execution_time_tracker, remove_none_args


class ActionType(str, Enum):
    PING = "ping"
    COUNT_ATOMS = "count_atoms"
    GET_ATOM = "get_atom"
    GET_NODE = "get_node"
    GET_LINK = "get_link"
    GET_LINKS = "get_links"
    GET_INCOMING_LINKS = "get_incoming_links"
    QUERY = "query"
    COMMIT_CHANGES = "commit_changes"


class Actions:
    def __init__(self) -> None:
        try:
            self.distributed_atom_space = DistributedAtomSpace(
                atomdb="redis_mongo",
                mongo_hostname=os.getenv("DAS_MONGODB_HOSTNAME"),
                mongo_port=int(os.getenv("DAS_MONGODB_PORT")),
                mongo_username=os.getenv("DAS_MONGODB_USERNAME"),
                mongo_password=os.getenv("DAS_MONGODB_PASSWORD"),
                redis_hostname=os.getenv("DAS_REDIS_HOSTNAME"),
                redis_port=int(os.getenv("DAS_REDIS_PORT")),
                mongo_tls_ca_file=os.getenv("DAS_MONGODB_TLS_CA_FILE"),
                redis_username=os.getenv("DAS_REDIS_USERNAME"),
                redis_password=os.getenv("DAS_REDIS_PASSWORD"),
                redis_cluster=os.getenv("DAS_USE_REDIS_CLUSTER") == "true",
                redis_ssl=os.getenv("DAS_USE_REDIS_SSL") == "true",
            )
        except Exception as e:
            raise UnreachableConnection(
                message="Exception at Actions: a connection could not be set up",
                details=str(e),
            )

    @execution_time_tracker
    def ping(self) -> dict:
        return dict(message="pong")

    @execution_time_tracker
    def count_atoms(self) -> Tuple[int, int]:
        return self.distributed_atom_space.count_atoms()

    @remove_none_args
    @execution_time_tracker
    def get_atom(
        self,
        handle: str,
    ) -> str | dict:
        return self.distributed_atom_space.get_atom(handle)

    @remove_none_args
    @execution_time_tracker
    def get_node(
        self,
        node_type: str,
        node_name: str,
    ) -> str | dict:
        return self.distributed_atom_space.get_node(
            node_type,
            node_name,
        )

    @remove_none_args
    @execution_time_tracker
    def get_link(
        self,
        link_type: str,
        link_targets: List[str],
    ) -> str | Dict:
        return self.distributed_atom_space.get_link(
            link_type,
            link_targets,
        )

    @remove_none_args
    @execution_time_tracker
    def get_links(
        self,
        link_type: str,
        target_types: List[str] = None,
        link_targets: List[str] = None,
    ) -> List[str] | List[Dict]:
        return self.distributed_atom_space.get_links(
            link_type,
            target_types,
            link_targets,
        )

    @remove_none_args
    @execution_time_tracker
    def get_incoming_links(
        self,
        atom_handle: str,
        kwargs,
    ) -> List[Tuple[dict, List[dict]] | dict]:
        return self.distributed_atom_space.get_incoming_links(
            atom_handle,
            **kwargs,
        )

    @execution_time_tracker
    @remove_none_args
    def query(
        self,
        query: Dict[str, Any],
        parameters: Dict[str, Any] | None = None,
    ) -> List[Dict[str, Any]]:
        return self.distributed_atom_space.query(query, parameters)

    @execution_time_tracker
    @remove_none_args
    def commit_changes(self) -> None:
        return self.distributed_atom_space.commit_changes()
