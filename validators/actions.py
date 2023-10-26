from incoming import datatypes, PayloadValidator


class NodeExistsValidator(PayloadValidator):
    node_type = datatypes.String()
    node_name = datatypes.String()


class LinkExistsValidator(PayloadValidator):
    link_type = datatypes.String()
    target_handles = datatypes.Array()


class GetNodeHandleValidator(PayloadValidator):
    node_type = datatypes.String()
    node_name = datatypes.String()


class GetLinkHandleValidator(PayloadValidator):
    link_type = datatypes.String()
    target_handles = datatypes.Array()


class GetLinkTargetsValidator(PayloadValidator):
    target_handle = datatypes.String()


class IsOrderedValidator(PayloadValidator):
    link_handle = datatypes.String()


class GetMatchedLinksValidator(PayloadValidator):
    link_type = datatypes.String()
    target_handles = datatypes.Array()
    extra_parameters = datatypes.JSON(dict)


class GetAllNodeValidator(PayloadValidator):
    link_type = datatypes.String()
    names = datatypes.Boolean()


class GetMatchedTypeTemplateValidator(PayloadValidator):
    template = datatypes.Array()
    extra_parameters = datatypes.JSON(dict)


class GetMatchedTypeValidator(PayloadValidator):
    link_type = datatypes.String()
    extra_parameters = datatypes.JSON(dict)


class GetNodeNameValidator(PayloadValidator):
    node_handle = datatypes.String()


class GetMatchedNodeNameValidator(PayloadValidator):
    node_type = datatypes.String()
    substring = datatypes.String()


class GetAtomAsDictValidator(PayloadValidator):
    handle = datatypes.String()
    arity = datatypes.Integer()


class GetAtomAsDeepRepresentationValidator(PayloadValidator):
    handle = datatypes.String()
    arity = datatypes.Integer()


class GetLinkTypeValidator(PayloadValidator):
    link_handle = datatypes.String()


class GetNodeTypeValidator(PayloadValidator):
    node_handle = datatypes.String()
