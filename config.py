import os


def load_env():
    environments = {
        "das-mongodb-name": "DAS_MONGODB_NAME",
        "das-mongodb-port": "DAS_MONGODB_PORT",
        "das-mongodb-hostname": "DAS_MONGODB_HOSTNAME",
        "das-mongodb-username": "DAS_MONGODB_USERNAME",
        "das-mongodb-password": "DAS_MONGODB_PASSWORD",
        "das-redis-hostname": "DAS_REDIS_HOSTNAME",
        "das-redis-port": "DAS_REDIS_PORT",
    }

    for key, value in environments.items():
        secret = "/var/openfaas/secrets/{key}"
        if os.path.exists(secret):
            with open(secret) as f:
                os.environ[value] = f.readline()
        else:
            os.environ[value] = os.environ[key]
