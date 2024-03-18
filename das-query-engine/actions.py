import os
from enum import Enum
from typing import Any, Dict, List, Tuple

from exceptions import UnreachableConnection
from hyperon_das import DistributedAtomSpace
from utils.decorators import execution_time_tracker, remove_none_args
from hyperon_das.logger import logger
from utils.version import compare_minor_versions

class HttpStatusCode(int, Enum):
    OK = 200
    CONFLICT = 409

class ActionType(str, Enum):
    PING = "ping"
    HANDSHAKE = "handshake"
    COUNT_ATOMS = "count_atoms"
    GET_ATOM = "get_atom"
    GET_NODE = "get_node"
    GET_LINK = "get_link"
    GET_LINKS = "get_links"
    GET_INCOMING_LINKS = "get_incoming_links"
    QUERY = "query"
    COMMIT_CHANGES = "commit_changes"
    CREATE_FIELD_INDEX = "create_field_index"


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
        return dict(message="pong"), HttpStatusCode.OK


    @execution_time_tracker
    def handshake(self, das_version: str, atomdb_version: str) -> dict:
        remote_info = self.distributed_atom_space.about()
        http_status_code = HttpStatusCode.OK

        remote_das_version = remote_info["das"]["version"]
        remote_atomdb_version = remote_info["atom_db"]["version"]

        comparison_das_version_result = compare_minor_versions(remote_das_version, das_version)
        if comparison_das_version_result is None or comparison_das_version_result != 0:
            logger().error(f"The version sent by the on-premises Hyperon-DAS is {das_version}, but the expected version on the remote server is {remote_das_version}.")
            http_status_code = HttpStatusCode.CONFLICT

        comparison_atomdb_version_result = compare_minor_versions(remote_atomdb_version, atomdb_version)
        if comparison_atomdb_version_result is None or comparison_atomdb_version_result != 0:
            logger().error(f"The version sent by the on-premises Hyperon-DAS-AtomDB is {atomdb_version}, but the expected version on the remote server is {remote_atomdb_version}.")
            http_status_code = HttpStatusCode.CONFLICT

        return remote_info, http_status_code


    @execution_time_tracker
    def count_atoms(self) -> Tuple[int, int]:
        return self.distributed_atom_space.count_atoms(), HttpStatusCode.OK

    @remove_none_args
    @execution_time_tracker
    def get_atom(
        self,
        handle: str,
    ) -> str | dict:
        return self.distributed_atom_space.get_atom(handle), HttpStatusCode.OK

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
        ), HttpStatusCode.OK

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
        ), HttpStatusCode.OK

    @remove_none_args
    @execution_time_tracker
    def get_links(
        self,
        link_type: str,
        target_types: List[str] = None,
        link_targets: List[str] = None,
        kwargs={},
    ) -> List[str] | List[Dict]:
        return self.distributed_atom_space.get_links(
            link_type,
            target_types,
            link_targets,
            **kwargs,
        ), HttpStatusCode.OK

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
        ), HttpStatusCode.OK

    @execution_time_tracker
    @remove_none_args
    def query(
        self,
        query: List[Dict[str, Any]] | Dict[str, Any],
        parameters: Dict[str, Any] = {"no_iterator": True},
    ) -> List[Dict[str, Any]]:
        return self.distributed_atom_space.query(query, parameters), HttpStatusCode.OK

    @execution_time_tracker
    @remove_none_args
    def commit_changes(self) -> None:
        return self.distributed_atom_space.commit_changes(), HttpStatusCode.OK
    
    @execution_time_tracker
    @remove_none_args
    def create_field_index(
        self,
        atom_type: str,
        field: str,
        type: str = None,
    ) -> str:
        response = self.distributed_atom_space.create_field_index(
            atom_type,
            field,
            type
        )
        return response, HttpStatusCode.OK
