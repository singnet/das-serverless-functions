from incoming import PayloadValidator, datatypes
from hyperon_das.das import logger


class HandshakeValidator(PayloadValidator):
    strict = True

    das_version = datatypes.String(required=True)
    atomdb_version = datatypes.String(required=True)


class GetAtomValidator(PayloadValidator):
    strict = True

    handle = datatypes.String(required=True)


class GetNodeValidator(PayloadValidator):
    strict = True

    node_type = datatypes.String(required=True)
    node_name = datatypes.String(required=True)


class GetLinkValidator(PayloadValidator):
    strict = True

    link_type = datatypes.String(required=True)
    link_targets = datatypes.Array(required=True)


class GetLinksValidator(PayloadValidator):
    strict = True

    link_type = datatypes.String(required=True)
    target_types = datatypes.Array(required=False)
    link_targets = datatypes.Array(required=False)
    kwargs = datatypes.Function(
        lambda value, *args, **kwargs: (
            isinstance(value, dict) if value is not None else True
        ),
        required=False,
    )


class GetIncomingLinksValidator(PayloadValidator):
    strict = True

    atom_handle = datatypes.String(required=True)
    kwargs = datatypes.Function(
        lambda value, *args, **kwargs: (
            isinstance(value, dict) if value is not None else True
        ),
        required=False,
    )


class QueryInputValidator(PayloadValidator):
    strict = True

    @staticmethod
    def validate_query(query, *args, **kwargs) -> bool:
        if not isinstance(query, dict):
            return False

        atom_type = query.get("atom_type")
        query_type = query.get("type")
        name = query.get("name")
        targets = query.get("targets")

        if atom_type not in ["node", "link"]:
            return False

        if not isinstance(query_type, str):
            return False

        if atom_type == "node" and not isinstance(name, str):
            return False

        if atom_type == "link" and not isinstance(targets, list):
            return False

        return True

    query = datatypes.Function(validate_query, required=True)

    parameters = datatypes.Function(
        lambda value, *args, **kwargs: (
            isinstance(value, dict) if value is not None else True
        ),
        required=False,
    )


class CreateFieldIndexValidator(PayloadValidator):
    strict = True

    atom_type = datatypes.String(required=True)
    field = datatypes.String(required=True)
    type = datatypes.Function(
        lambda value, *args, **kwargs: (
            isinstance(value, str) if value is not None else True
        ),
        required=False,
    )
    composite_type = datatypes.Function(
        lambda value, *args, **kwargs: (
            isinstance(value, list) if value is not None else True
        ),
        required=False,
    )


class CustomQueryValidator(PayloadValidator):
    strict = True

    index_id = datatypes.String(required=True)
    kwargs = datatypes.Function(
        lambda value, *args, **kwargs: (
            isinstance(value, dict) if value is not None else True
        ),
        required=False,
    )


class FetchValidator(PayloadValidator):
    strict = True

    query = datatypes.Function(
        lambda value, *args, **kwargs: (
            (isinstance(value, dict) or all(isinstance(item, dict) for item in value))
            if value is not None
            else True
        ),
        required=False,
    )
    host = datatypes.Function(
        lambda value, *args, **kwargs: (
            isinstance(value, str) if value is not None else True
        ),
        required=False,
    )
    port = datatypes.Function(
        lambda value, *args, **kwargs: (
            isinstance(value, int) if value is not None else True
        ),
        required=False,
    )
    kwargs = datatypes.Function(
        lambda value, *args, **kwargs: (
            isinstance(value, dict) if value is not None else True
        ),
        required=False,
    )


class CreateContextValidator(PayloadValidator):
    strict = True

    name = datatypes.String(required=True)
    query = datatypes.Function(
        lambda value, *args, **kwargs: (
            (isinstance(value, dict) or all(isinstance(item, dict) for item in value))
            if value is not None
            else True
        ),
        required=True,
    )


class CommitChangesValidator(PayloadValidator):
    strict = True

    kwargs = datatypes.Function(
        lambda value, *args, **kwargs: (
            isinstance(value, dict) if value is not None else True
        ),
        required=False,
    )
