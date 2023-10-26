from hyperon_das_atomdb.adapters import RedisMongoDB

redis_mongo_db = RedisMongoDB()


def node_exists(node_type: str, node_name: str) -> bool:
    return redis_mongo_db.node_exists(node_type, node_name)


def link_exists(link_type: str, target_handles: list(str)) -> bool:
    return redis_mongo_db.link_exists(link_type, target_handles)


def get_node_handle(node_type: str, node_name: str) -> str:
    return redis_mongo_db.get_node_handle(node_type, node_name)


def get_link_handle(link_type: str, target_handles: list(str)) -> str:
    return redis_mongo_db.get_link_handle(link_type, target_handles)


def get_link_targets(link_handle: str) -> list(str):
    return redis_mongo_db.get_link_targets(link_handle)


def is_ordered(link_handle: str) -> bool:
    return redis_mongo_db.is_ordered(link_handle)


def get_matched_links(
    link_type: str,
    target_handles: list(str),
    extra_parameters: dict | None = None,
):
    return redis_mongo_db.get_matched_links(link_type, target_handles, extra_parameters)


def get_all_nodes(node_type: str, names: bool = False) -> list(str):
    return redis_mongo_db.get_all_nodes(node_type, names)


def get_matched_type_template(
    template: list,
    extra_parameters: dict = None,
) -> list(str):
    return redis_mongo_db.get_matched_type_template(template, extra_parameters)


def get_matched_type(
    link_type: str,
    extra_parameters: dict = None,
) -> list(str):
    return redis_mongo_db.get_matched_type(link_type, extra_parameters)


def get_node_name(node_handle: str) -> str:
    return redis_mongo_db.get_node_name(node_handle)


def get_matched_node_name(node_type: str, substring: str) -> str:
    return redis_mongo_db.get_matched_node_name(node_type, substring)


def get_atom_as_dict(handle, arity=-1) -> dict:
    return redis_mongo_db.get_atom_as_dict(handle, arity)


def get_atom_as_deep_representation(
    handle: str,
    arity=-1,
) -> str:
    return redis_mongo_db.get_atom_as_deep_representation(handle, arity)


def get_link_type(link_handle: str) -> str:
    return redis_mongo_db.get_link_type(link_handle)


def get_node_type(node_handle: str) -> str:
    return redis_mongo_db.get_node_type(node_handle)


def count_atoms(self) -> tuple([int, int]):
    return redis_mongo_db.count_atoms()


def clear_database(self) -> None:
    return redis_mongo_db.clear_database()
