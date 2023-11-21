import os
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
        "dasmongodbname": "DAS_MONGODB_NAME",
        "dasmongodbport": "DAS_MONGODB_PORT",
        "dasmongodbhostname": "DAS_MONGODB_HOSTNAME",
        "dasmongodbusername": "DAS_MONGODB_USERNAME",
        "dasmongodbpassword": "DAS_MONGODB_PASSWORD",
        "dasredishostname": "DAS_REDIS_HOSTNAME",
        "dasredisport": "DAS_REDIS_PORT",
        "dasredispassword": "DAS_REDIS_PASSWORD",
        "dasredisusername": "DAS_REDIS_USERNAME",
        "dasmongodbtlscafile": "DAS_MONGODB_TLS_CA_FILE",
        "dasuserediscluster": "DAS_USE_REDIS_CLUSTER",
        "dasusecachednodes": "DAS_USE_CACHED_NODES",
        "dasusecachedlinktypes": "DAS_USE_CACHED_LINK_TYPES",
        "dasusecachednodetypes": "DAS_USE_CACHED_NODE_TYPES",
    }

    for key, value in environments.items():
        secret = f"/var/openfaas/secrets/{key}"
        if os.path.exists(secret):
            with open(secret) as f:
                os.environ[value] = f.readline().strip()
        else:
            env_value = os.environ.get(key, None)
            # if env_value is None:
            #     raise Exception(f"Environment variable {key} is empty")
            os.environ[value] = env_value if isinstance(env_value, str) else ""


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
