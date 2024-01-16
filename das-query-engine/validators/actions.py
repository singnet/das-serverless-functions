from incoming import PayloadValidator, datatypes


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
    target_types = datatypes.String(required=False)
    link_targets = datatypes.Array(required=False)


class GetIncomingLinksValidator(PayloadValidator):
    strict = True

    atom_handle = datatypes.String(required=True)
    handles_only = datatypes.Boolean(required=False)


class QueryValidator(PayloadValidator):
    strict = True

    query = datatypes.Function(
        lambda value, *args, **kwargs: isinstance(value, dict),
        required=True,
    )

    parameters = datatypes.Function(
        lambda value, *args, **kwargs: isinstance(value, dict) if value is not None else True,
        required=False,
    )
