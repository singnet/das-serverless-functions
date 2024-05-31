import os
from enum import Enum
from typing import Any, Dict, List, Tuple
from http import HTTPStatus
from exceptions import UnreachableConnection
from hyperon_das import DistributedAtomSpace
from hyperon_das import exceptions as das_exceptions
from hyperon_das_atomdb import exceptions as atom_db_exceptions
from utils.decorators import execution_time_tracker, remove_none_args
from hyperon_das.logger import logger
from utils.version import compare_minor_versions


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
    CUSTOM_QUERY = "custom_query"
    FETCH = "fetch"
    CREATE_CONTEXT = "create_context"


class Actions:
    def __init__(self) -> None:
        try:
            self.das = DistributedAtomSpace(
                system_parameters={'running_on_server': True},
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
    def ping(self) -> Tuple[dict, int]:
        return dict(message="pong"), HTTPStatus.OK

    @execution_time_tracker
    def handshake(self, das_version: str, atomdb_version: str) -> Tuple[dict, int]:
        remote_info = self.das.about()
        http_status_code = HTTPStatus.OK

        remote_das_version = remote_info["das"]["version"]
        remote_atomdb_version = remote_info["atom_db"]["version"]

        comparison_das_version_result = compare_minor_versions(remote_das_version, das_version)
        if comparison_das_version_result is None or comparison_das_version_result != 0:
            logger().error(f"The version sent by the on-premises Hyperon-DAS is {das_version}, but the expected version on the remote server is {remote_das_version}.")
            http_status_code = HTTPStatus.CONFLICT

        comparison_atomdb_version_result = compare_minor_versions(remote_atomdb_version, atomdb_version)
        if comparison_atomdb_version_result is None or comparison_atomdb_version_result != 0:
            logger().error(f"The version sent by the on-premises Hyperon-DAS-AtomDB is {atomdb_version}, but the expected version on the remote server is {remote_atomdb_version}.")
            http_status_code = HTTPStatus.CONFLICT

        return remote_info, http_status_code

    @execution_time_tracker
    def count_atoms(self) -> Tuple[Tuple[int, int], int]:
        return self.das.count_atoms(), HTTPStatus.OK

    @remove_none_args
    @execution_time_tracker
    def get_atom(
        self,
        handle: str,
    ) -> Tuple[str | dict, int]:
        try:
            return self.das.get_atom(handle), HTTPStatus.OK
        except atom_db_exceptions.AtomDoesNotExist as e:
            return str(e), HTTPStatus.NOT_FOUND
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @remove_none_args
    @execution_time_tracker
    def get_node(
        self,
        node_type: str,
        node_name: str,
    ) -> Tuple[str | dict, int]:
        try:
            return self.das.get_node(node_type, node_name), HTTPStatus.OK
        except atom_db_exceptions.NodeDoesNotExist as e:
            return str(e), HTTPStatus.NOT_FOUND
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @remove_none_args
    @execution_time_tracker
    def get_link(
        self,
        link_type: str,
        link_targets: List[str],
    ) -> Tuple[str | Dict, int]:
        try:
            return self.das.get_link(link_type, link_targets), HTTPStatus.OK
        except atom_db_exceptions.LinkDoesNotExist as e:
            return str(e), HTTPStatus.NOT_FOUND
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @remove_none_args
    @execution_time_tracker
    def get_links(
        self,
        link_type: str,
        target_types: List[str] = None,
        link_targets: List[str] = None,
        kwargs={},
    ) -> Tuple[List[str | dict], int]:
        try:
            return self.das.get_links(link_type, target_types, link_targets, **kwargs), HTTPStatus.OK
        except (atom_db_exceptions.LinkDoesNotExist, atom_db_exceptions.AtomDoesNotExist) as e:
            return str(e), HTTPStatus.NOT_FOUND
        except ValueError as e:
            return str(e), HTTPStatus.BAD_REQUEST
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @remove_none_args
    @execution_time_tracker
    def get_incoming_links(
        self,
        atom_handle: str,
        kwargs,
    ) -> Tuple[List[Tuple[dict, List[dict]] | dict], int]:
        try:
            return self.das.get_incoming_links(atom_handle, **kwargs), HTTPStatus.OK
        except (atom_db_exceptions.AtomDoesNotExist) as e:
            return str(e), HTTPStatus.NOT_FOUND
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @execution_time_tracker
    @remove_none_args
    def query(
        self,
        query: List[Dict[str, Any]] | Dict[str, Any],
        parameters: Dict[str, Any] = {"no_iterator": True},
    ) -> Tuple[List[Dict[str, Any]], int]:
        try:
            return self.das.query(query, parameters), HTTPStatus.OK
        except (atom_db_exceptions.LinkDoesNotExist, atom_db_exceptions.AtomDoesNotExist) as e:
            return str(e), HTTPStatus.NOT_FOUND
        except (das_exceptions.UnexpectedQueryFormat, ValueError) as e:
            return str(e), HTTPStatus.BAD_REQUEST
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @execution_time_tracker
    def commit_changes(self, kwargs={}) -> Tuple[None, int]:
        try:
            return self.das.commit_changes(**kwargs), HTTPStatus.OK
        except atom_db_exceptions.InvalidOperationException as e:
            return str(e), HTTPStatus.FORBIDDEN
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR
    
    @execution_time_tracker
    def create_field_index(
        self,
        atom_type: str,
        field: str,
        type: str = None,
        composite_type: List[Any] = None,
    ) -> Tuple[str, int]:
        try:
            response = self.das.create_field_index(atom_type=atom_type, field=field, type=type, composite_type=composite_type)
            return response, HTTPStatus.OK
        except ValueError as e:
            return str(e), HTTPStatus.BAD_REQUEST
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @execution_time_tracker
    def custom_query(
        self,
        index_id: str,
        kwargs={}
    ) -> Tuple[str, int]:
        try:
            response = self.das.custom_query(
                index_id,
                **kwargs
            )
            return response, HTTPStatus.OK
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR
    
    @execution_time_tracker
    def fetch(
        self, query: List[dict] | dict = None, host: str = None, port: int = None, kwargs={}
    ) -> Tuple[bool, int]:
        try:
            response = self.das.fetch(query=query, host=host, port=port, **kwargs)
            return response, HTTPStatus.OK
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @execution_time_tracker
    def create_context(
        self, name: str, queries: List[list[dict] | dict] = []
    ) -> Tuple[bool, int]:
        try:
            response = self.das.create_context(name=name, queries=queries)
            return response, HTTPStatus.OK
        except (atom_db_exceptions.LinkDoesNotExist, atom_db_exceptions.AtomDoesNotExist) as e:
            return str(e), HTTPStatus.NOT_FOUND
        except (atom_db_exceptions.AddNodeException, das_exceptions.UnexpectedQueryFormat, ValueError) as e:
            return str(e), HTTPStatus.BAD_REQUEST
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR
