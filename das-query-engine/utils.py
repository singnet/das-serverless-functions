import os
from logger import Logger
from functools import wraps
from hyperon_das.pattern_matcher import (
    LogicalExpression,
    Variable,
    Node,
    Link,
    Or,
    And,
    Not,
)


def load_env():
    environments = {
        "dasmongodbname": {
            "key": "DAS_MONGODB_NAME",
            "hidden": False,
            "required": True,
        },
        "dasmongodbport": {
            "key": "DAS_MONGODB_PORT",
            "hidden": False,
            "required": True,
        },
        "dasmongodbhostname": {
            "key": "DAS_MONGODB_HOSTNAME",
            "hidden": False,
            "required": True,
        },
        "dasmongodbusername": {
            "key": "DAS_MONGODB_USERNAME",
            "hidden": True,
            "required": True,
        },
        "dasmongodbpassword": {
            "key": "DAS_MONGODB_PASSWORD",
            "hidden": True,
            "required": True,
        },
        "dasredishostname": {
            "key": "DAS_REDIS_HOSTNAME",
            "hidden": False,
            "required": True,
        },
        "dasredisport": {
            "key": "DAS_REDIS_PORT",
            "hidden": False,
            "required": True,
        },
        "dasredispassword": {
            "key": "DAS_REDIS_PASSWORD",
            "hidden": True,
            "required": False,
        },
        "dasredisusername": {
            "key": "DAS_REDIS_USERNAME",
            "hidden": True,
            "required": False,
        },
        "dasuseredisssl": {
            "key": "DAS_USE_REDIS_SSL",
            "hidden": False,
            "required": False,
        },
        "dasmongodbtlscafile": {
            "key": "DAS_MONGODB_TLS_CA_FILE",
            "hidden": False,
            "required": False,
        },
        "dasuserediscluster": {
            "key": "DAS_USE_REDIS_CLUSTER",
            "hidden": False,
            "required": False,
        },
        "dasusecachednodes": {
            "key": "DAS_USE_CACHED_NODES",
            "hidden": False,
            "required": False,
        },
        "dasusecachedlinktypes": {
            "key": "DAS_USE_CACHED_LINK_TYPES",
            "hidden": False,
            "required": False,
        },
        "dasusecachednodetypes": {
            "key": "DAS_USE_CACHED_NODE_TYPES",
            "hidden": False,
            "required": False,
        },
    }

    for key, value in environments.items():
        secret = f"/var/openfaas/secrets/{key}"
        env_value = None

        if os.path.exists(secret):
            with open(secret) as f:
                env_value = f.readline().strip()
        else:
            env_value = os.environ.get(key, "")

        os.environ[value["key"]] = env_value if isinstance(env_value, str) else ""

        if value["required"] and not env_value:
            error_message = f"Environment variable {key} is empty"
            logger().error(error_message)
            raise Exception(error_message)

        env_value_display = "*****" if value["hidden"] else env_value
        logger().info(f'{value["key"]} - {env_value_display}')


class LogicalExpressionParser:
    def from_dict(self, query: dict) -> LogicalExpression:
        key = next(iter(query))
        value = query[key]

        if key == "Variable":
            return Variable(value["variable_name"])
        elif key == "Node":
            return Node(value["node_type"], value["node_name"])
        elif key == "Link":
            ordered = value.get("ordered", True)
            targets = [self.from_dict(target) for target in value["targets"]]
            return Link(value["link_type"], targets, ordered)
        elif key == "And":
            conditions = [self.from_dict(condition) for condition in value]
            return And(conditions)
        elif key == "Or":
            conditions = [self.from_dict(condition) for condition in value]
            return Or(conditions)
        elif key == "Not":
            condition = self.from_dict(value)
            return Not(condition)


def remove_none_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        new_args = [arg for arg in args if arg is not None]
        new_kwargs = {key: value for key, value in kwargs.items() if value is not None}
        return func(*new_args, **new_kwargs)

    return wrapper


def logger():
    return Logger.get_instance()
