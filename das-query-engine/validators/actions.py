from incoming import PayloadValidator, datatypes


class GetAtomValidator(PayloadValidator):
    strict = True

    handle = datatypes.String(required=True)


class CountAtomsValidator(PayloadValidator):
    strict = True

    parameters = datatypes.Function(
        lambda value, *args, **kwargs: (isinstance(value, dict) if value is not None else True),
        required=False,
    )


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

    link_filter = datatypes.Function(
        lambda value, *args, **kwargs: (isinstance(value, dict) if value is not None else True),
        required=True,
    )


class GetIncomingLinksValidator(PayloadValidator):
    strict = True

    atom_handle = datatypes.String(required=True)
    kwargs = datatypes.Function(
        lambda value, *args, **kwargs: (isinstance(value, dict) if value is not None else True),
        required=False,
    )


class QueryValidator(PayloadValidator):
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
        lambda value, *args, **kwargs: (isinstance(value, dict) if value is not None else True),
        required=False,
    )


class CreateFieldIndexValidator(PayloadValidator):
    strict = True

    atom_type = datatypes.String(required=True)
    fields = datatypes.Function(
        lambda value, *args, **kwargs: (isinstance(value, list)),
        required=True,
    )
    named_type = datatypes.Function(
        lambda value, *args, **kwargs: (isinstance(value, str) if value is not None else True),
        required=False,
    )
    composite_type = datatypes.Function(
        lambda value, *args, **kwargs: (isinstance(value, list) if value is not None else True),
        required=False,
    )
    index_type = datatypes.String(required=False)


class CustomQueryValidator(PayloadValidator):
    strict = True

    index_id = datatypes.String(required=True)
    query = datatypes.Function(
        lambda value, *args, **kwargs: isinstance(value, dict), required=True
    )
    kwargs = datatypes.Function(
        lambda value, *args, **kwargs: (isinstance(value, dict) if value is not None else True),
        required=False,
    )


class GetAtomsByField(PayloadValidator):
    strict = True

    query = datatypes.Function(
        lambda value, *args, **kwargs: (isinstance(value, dict)), required=True
    )


class GetAtomsByTextField(PayloadValidator):
    strict = True

    text_value = datatypes.String(required=True)
    field = datatypes.String(required=False)
    text_index_id = datatypes.String(required=False)


class GetNodeByNameStartingWith(PayloadValidator):
    strict = True
    node_type = datatypes.String(required=True)
    startswith = datatypes.String(required=False)


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
        lambda value, *args, **kwargs: (isinstance(value, str) if value is not None else True),
        required=False,
    )
    port = datatypes.Function(
        lambda value, *args, **kwargs: (isinstance(value, int) if value is not None else True),
        required=False,
    )
    kwargs = datatypes.Function(
        lambda value, *args, **kwargs: (isinstance(value, dict) if value is not None else True),
        required=False,
    )


class CreateContextValidator(PayloadValidator):
    strict = True

    name = datatypes.String(required=True)
    queries = datatypes.Function(
        lambda value, *args, **kwargs: (
            (all(isinstance(item, dict) or isinstance(item, list) for item in value))
            if value is not None
            else True
        ),
        required=False,
    )


class CommitChangesValidator(PayloadValidator):
    strict = True

    kwargs = datatypes.Function(
        lambda value, *args, **kwargs: (isinstance(value, dict) if value is not None else True),
        required=False,
    )
