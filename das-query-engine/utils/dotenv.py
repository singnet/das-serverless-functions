import os

from config import env_schema
from hyperon_das.logger import logger


def load_env():
    env_log_entries = []

    for var, constraints in env_schema.items():
        var_value = os.environ.get(var, "")

        if constraints["required"] and not var_value:
            error_message = f"Environment variable {var} is empty"
            logger().error(error_message)
            raise Exception(error_message)

        var_value_display = (
            "*****" if constraints["hidden"] else var_value if var_value != "" else "(empty)"
        )
        env_log_entries.append(f"{var} - {var_value_display}")

    logger().info("\n".join(env_log_entries))
