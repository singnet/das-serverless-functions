from incoming import datatypes, PayloadValidator


class GetAtomValidator(PayloadValidator):
    handle = datatypes.String(required=True)
    output_format = datatypes.String(required=False)


class GetNodeValidator(PayloadValidator):
    node_type = datatypes.String(required=True)
    node_name = datatypes.String(required=True)
    output_format = datatypes.String(required=False)


class GetNodesValidator(PayloadValidator):
    node_type = datatypes.String(required=True)
    node_name = datatypes.String(required=True)
    output_format = datatypes.String(required=False)


class GetLinkValidator(PayloadValidator):
    link_type = datatypes.String(required=True)
    targets = datatypes.Array(required=False)
    output_format = datatypes.String(required=False)


class GetLinksValidator(PayloadValidator):
    link_type = datatypes.String(required=True)
    target_types = datatypes.Array(required=False)
    targets = datatypes.Array(required=False)
    output_format = datatypes.String(required=False)


class GetLinkTypeValidator(PayloadValidator):
    link_handle = datatypes.String(required=True)


class GetLinkTargetsValidator(PayloadValidator):
    link_handle = datatypes.String(required=True)


class GetNodeTypeValidator(PayloadValidator):
    node_handle = datatypes.String(required=True)


class QueryValidator(PayloadValidator):
    query = datatypes.Function(
        lambda value, *args, **kwargs: isinstance(value, dict),
        required=True,
    )
    output_format = datatypes.String(required=False)


class PatternMatcherQueryValidator(PayloadValidator):
    query = datatypes.Function(
        lambda value, *args, **kwargs: isinstance(value, dict),
        required=True,
    )
    output_format = datatypes.String(required=False)


class AddNodeValidator(PayloadValidator):
    node_params = datatypes.Function(
        lambda value, *args, **kwargs: isinstance(value, dict),
        required=True,
    )


class AddLinkValidator(PayloadValidator):
    link_params = datatypes.Function(
        lambda value, *args, **kwargs: isinstance(value, dict),
        required=True,
    )
