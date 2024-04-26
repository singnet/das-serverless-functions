#!/bin/bash

set -e

function unit_tests() {
    python3 -m pytest -sx -vv das-query-engine/tests/unit
}

function unit_tests_coverage() {
    python3 -m pytest -sx -vv das-query-engine/tests/unit --cov=./ --cov-report=term-missing --cov-fail-under=70
}

function integration_tests() {
    local OPENFAAS_CONTAINER_MAX_ATTEMPS=5
    local OPENFAAS_CONTAINER_ATTEMPS=0

    local OPENFAAS_CONTAINER="openfaas"

    local QUERY_ENGINE_SERVICE="query-engine"

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

    while ! docker exec "$OPENFAAS_CONTAINER" pgrep -f "$QUERY_ENGINE_SERVICE" >/dev/null; do
        OPENFAAS_EXIT_CODE=$(docker inspect --format='{{.State.ExitCode}}' "$OPENFAAS_CONTAINER")

        if [ "$OPENFAAS_CONTAINER_ATTEMPS" -gt "$OPENFAAS_CONTAINER_MAX_ATTEMPS" ]; then
            echo "Exceeded maximum attempts to start the container $OPENFAAS_CONTAINER"
            docker logs "$OPENFAAS_CONTAINER"
            exit 1
        fi

        if [ "$OPENFAAS_EXIT_CODE" -gt 0 ]; then
            echo "The container $OPENFAAS_CONTAINER exited with status code $OPENFAAS_EXIT_CODE"
            docker logs "$OPENFAAS_CONTAINER"
            exit 1
        fi

        echo "Waiting for $QUERY_ENGINE_SERVICE in container $OPENFAAS_CONTAINER to start..."

        OPENFAAS_CONTAINER_ATTEMPS=$(($OPENFAAS_CONTAINER_ATTEMPS + 1))

        sleep 10
    done

    docker exec --tty $OPENFAAS_CONTAINER sh -c "docker exec --tty $QUERY_ENGINE_SERVICE sh -c 'python3 -m pytest -sx -vv tests/integration'"

    docker compose down
}

if [ "$1" == "integration" ]; then
    integration_tests
elif [ "$1" == "unit" ]; then
    unit_tests
elif [ "$1" == "unit-coverage" ]; then
    unit_tests_coverage
fi
