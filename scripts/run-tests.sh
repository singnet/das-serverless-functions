#!/bin/bash

set -e

OPENFAAS_CONTAINER="openfaas"

QUERY_ENGINE_SERVICE="query-engine"

docker compose down

if ! docker ps --format '{{.Names}}' | grep -q "$OPENFAAS_CONTAINER"; then
    if [ -z "$REMOTE" ]; then
        docker compose up -d --build --force-recreate
        echo "Initializing the OpenFaaS and required containers for local connection..."
    else
        docker compose up -d --build --force-recreate openfaas
        echo "Initializing the OpenFaaS container for remote database connection..."
    fi
    unset REMOTE
fi

while ! docker exec $OPENFAAS_CONTAINER pgrep -f $QUERY_ENGINE_SERVICE >/dev/null; do
    echo "Waiting for $QUERY_ENGINE_SERVICE in container $OPENFAAS_CONTAINER to start..."
    sleep 10
done

if [ "$1" = 'unit-tests-coverage' ]; then
    TEST_COMMAND="python3 -m pytest -sx -vv tests/unit --cov=./ --cov-report=term-missing --cov-fail-under=70"
else
    TEST_COMMAND="python3 -m pytest -sx -vv tests/$1"
fi

docker exec --tty $OPENFAAS_CONTAINER sh -c "docker exec --tty $QUERY_ENGINE_SERVICE sh -c '$TEST_COMMAND'"

docker compose down
