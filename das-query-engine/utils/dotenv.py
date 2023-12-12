import os
from config import env_schema
from hyperon_das.logger import logger


def load_env():
    env_log_entries = []

    for key, value in env_schema.items():
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

        env_value_display = (
            "*****" if value["hidden"] else env_value if env_value != "" else "(empty)"
        )
        env_log_entries.append(f'{value["key"]} - {env_value_display}')

    logger().info("\n".join(env_log_entries))
