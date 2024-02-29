from incoming import PayloadValidator, datatypes


class HandshakeValidator(PayloadValidator):
    strict = True

    version = datatypes.String(required=True) # TODO: add the payload here 

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
        lambda value, *args, **kwargs: isinstance(value, dict) if value is not None else True,
        required=False,
    )

class GetIncomingLinksValidator(PayloadValidator):
    strict = True

    atom_handle = datatypes.String(required=True)
    kwargs = datatypes.Function(
        lambda value, *args, **kwargs: isinstance(value, dict) if value is not None else True,
        required=False,
    )


class QueryValidator(PayloadValidator):
    strict = True

    query = datatypes.Function(
        lambda value, *args, **kwargs: isinstance(value, dict) or all(isinstance(item, dict) for item in value),
        required=True,
    )

    parameters = datatypes.Function(
        lambda value, *args, **kwargs: isinstance(value, dict) if value is not None else True,
        required=False,
    )
