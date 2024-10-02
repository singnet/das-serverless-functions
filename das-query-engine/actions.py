import os
from enum import Enum
from http import HTTPStatus
from typing import Any, Dict, List, Tuple

from exceptions import UnreachableConnection
from hyperon_das import DistributedAtomSpace
from hyperon_das import exceptions as das_exceptions
from hyperon_das.logger import logger
import hyperon_das.link_filters as link_filters
from hyperon_das_atomdb import exceptions as atom_db_exceptions
from utils.decorators import execution_time_tracker, remove_none_args


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
    GET_ATOMS_BY_FIELD = "get_atoms_by_field"
    GET_ATOMS_BY_TEXT_FIELD = "get_atoms_by_text_field"
    GET_NODE_BY_NAME_STARTING_WITH = "get_node_by_name_starting_with"


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
    def handshake(self) -> Tuple[dict, int]:
        remote_info = self.das.about()
        http_status_code = HTTPStatus.OK

        return remote_info, http_status_code

    @execution_time_tracker
    def count_atoms(self, parameters: Dict[str, Any] = None) -> Tuple[Dict[str, int], int]:
        return self.das.count_atoms(parameters), HTTPStatus.OK

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
        except atom_db_exceptions.AtomDoesNotExist as e:
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
        except atom_db_exceptions.AtomDoesNotExist as e:
            return str(e), HTTPStatus.NOT_FOUND
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @remove_none_args
    @execution_time_tracker
    def get_links(
        self,
        link_filter: dict = {}
    ) -> Tuple[List[str | dict], int] | Tuple[str, int]:
        if link_filter["filter_type"] == link_filters.LinkFilterType.FLAT_TYPE_TEMPLATE:
            link_filter_obj = link_filters.FlatTypeTemplate(
                link_filter["target_types"],
                link_filter["link_type"],
                link_filter["toplevel_only"])
        elif link_filter["filter_type"] == link_filters.LinkFilterType.NAMED_TYPE:
            link_filter_obj = link_filters.NamedType(
                link_filter["link_type"],
                link_filter["toplevel_only"])
        elif link_filter["filter_type"] == link_filters.LinkFilterType.TARGETS:
            link_filter_obj = link_filters.Targets(
                link_filter["targets"],
                link_filter["link_type"],
                link_filter["toplevel_only"])
        else:
            return f"Invalid link_filter object: {link_filter_obj}", HTTPStatus.BAD_REQUEST
        try:
            return (
                self.das.get_links(link_filter_obj),
                HTTPStatus.OK,
            )
        except atom_db_exceptions.AtomDoesNotExist as e:
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
    ) -> Tuple[List[Tuple[dict, List[dict]] | dict], int] | Tuple[str, int]:
        try:
            return self.das.get_incoming_links(atom_handle, **kwargs), HTTPStatus.OK
        except atom_db_exceptions.AtomDoesNotExist as e:
            return str(e), HTTPStatus.NOT_FOUND
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @execution_time_tracker
    @remove_none_args
    def query(
        self,
        query: List[Dict[str, Any]] | Dict[str, Any],
        parameters: Dict[str, Any] = {"no_iterator": True},
    ) -> Tuple[List[Dict[str, Any]], int] | Tuple[str, int]:
        try:
            return self.das.query(query, parameters), HTTPStatus.OK
        except atom_db_exceptions.AtomDoesNotExist as e:
            return str(e), HTTPStatus.NOT_FOUND
        except (das_exceptions.UnexpectedQueryFormat, ValueError) as e:
            return str(e), HTTPStatus.BAD_REQUEST
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @execution_time_tracker
    @remove_none_args
    def get_atoms_by_field(
        self,
        query: Dict[str, Any],
    ) -> Tuple[List[str], int] | Tuple[str, int]:
        try:
            return self.das.get_atoms_by_field(query), HTTPStatus.OK
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @execution_time_tracker
    @remove_none_args
    def get_atoms_by_text_field(
        self, text_value: str, field: str = None, text_index_id: str = None
    ) -> Tuple[List[str], int] | Tuple[str, int]:
        try:
            return self.das.get_atoms_by_text_field(text_value, field, text_index_id), HTTPStatus.OK
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @execution_time_tracker
    @remove_none_args
    def get_node_by_name_starting_with(
        self, node_type: str, startswith: str
    ) -> Tuple[List[str], int] | Tuple[str, int]:
        try:
            return self.das.get_node_by_name_starting_with(node_type, startswith), HTTPStatus.OK
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @execution_time_tracker
    def commit_changes(self, kwargs={}) -> Tuple[None, int] | Tuple[str, int]:
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
        fields: List[str],
        named_type: str = None,
        composite_type: List[Any] = None,
        index_type: str = None,
    ) -> Tuple[str, int]:
        try:
            response = self.das.create_field_index(
                atom_type=atom_type,
                fields=fields,
                named_type=named_type,
                composite_type=composite_type,
                index_type=index_type,
            )
            return response, HTTPStatus.OK
        except ValueError as e:
            return str(e), HTTPStatus.BAD_REQUEST
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @execution_time_tracker
    def custom_query(self, index_id: str, query: Dict[str, Any], kwargs={}) -> Tuple[str, int]:
        try:
            response = self.das.custom_query(index_id, query, **kwargs)
            return response, HTTPStatus.OK
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @execution_time_tracker
    def fetch(
        self, query: List[dict] | dict = None, host: str = None, port: int = None, kwargs={}
    ) -> Tuple[bool, int] | Tuple[str, int]:
        try:
            response = self.das.fetch(query=query, host=host, port=port, **kwargs)
            return response, HTTPStatus.OK
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR

    @execution_time_tracker
    def create_context(
        self, name: str, queries: List[list[dict] | dict] = []
    ) -> Tuple[bool, int] | Tuple[str, int]:
        try:
            response = self.das.create_context(name=name, queries=queries)
            return response, HTTPStatus.OK
        except atom_db_exceptions.AtomDoesNotExist as e:
            return str(e), HTTPStatus.NOT_FOUND
        except (
            atom_db_exceptions.AddNodeException,
            das_exceptions.UnexpectedQueryFormat,
            ValueError,
        ) as e:
            return str(e), HTTPStatus.BAD_REQUEST
        except Exception as e:
            return str(e), HTTPStatus.INTERNAL_SERVER_ERROR
