import os


def load_env():
    environments = {
        "dasmongodbname": "DAS_MONGODB_NAME",
        "dasmongodbport": "DAS_MONGODB_PORT",
        "dasmongodbhostname": "DAS_MONGODB_HOSTNAME",
        "dasmongodbusername": "DAS_MONGODB_USERNAME",
        "dasmongodbpassword": "DAS_MONGODB_PASSWORD",
        "dasredishostname": "DAS_REDIS_HOSTNAME",
        "dasredisport": "DAS_REDIS_PORT",
    }

    for key, value in environments.items():
        secret = "/var/openfaas/secrets/{key}"
        if os.path.exists(secret):
            with open(secret) as f:
                os.environ[value] = f.readline().strip()
        else:
            env_value = os.environ.get(key, None)
            if env_value is None:
                raise Exception(f"Environment variable {os.environ[value]} is empty")
            os.environ[value] = env_value


load_env()
