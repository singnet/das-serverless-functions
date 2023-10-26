import os


def load_env():
    environments = {
        "das_mongodb_name": "DAS_MONGODB_NAME",
        "das_mongodb_port": "DAS_MONGODB_PORT",
        "das_mongodb_hostname": "DAS_MONGODB_HOSTNAME",
        "das_mongodb_username": "DAS_MONGODB_USERNAME",
        "das_mongodb_password": "DAS_MONGODB_PASSWORD",
        "das_redis_hostname": "DAS_REDIS_HOSTNAME",
        "das_redis_port": "DAS_REDIS_PORT",
    }

    for key, value in environments.items():
        secret = "/var/openfaas/secrets/{key}"
        if os.path.exists(secret):
            with open(secret) as f:
                os.environ[value] = f.readline()
        else:
            os.environ[value] = os.environ[key]

    