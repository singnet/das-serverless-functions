#!/bin/bash

set -e

OPENFAAS_CONTAINER="openfaas"

QUERY_ENGINE_SERVICE="query-engine"

if ! docker ps --format '{{.Names}}' | grep -q "$OPENFAAS_CONTAINER"; then
    docker compose up -d --build
fi

while ! docker exec $OPENFAAS_CONTAINER pgrep -f $QUERY_ENGINE_SERVICE > /dev/null; do
    echo "Waiting for $QUERY_ENGINE_SERVICE in container $OPENFAAS_CONTAINER to start..."
    sleep 10
done

docker exec -it $OPENFAAS_CONTAINER sh -c "docker exec -it $QUERY_ENGINE_SERVICE sh -c 'python3 -m pytest --verbose tests/$1'"

