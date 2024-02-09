#!/bin/sh

set -e

if docker info >/dev/null 2>&1; then
	echo "Dockerd is running."
else
	dockerd &

	until docker info >/dev/null 2>&1; do
		echo "Waiting for dockerd to start..."
		sleep 1
	done
fi

faas-cli build

FUNCTION_NAME=$(grep -A6 "^functions:" "./stack.yml" | grep -E "^ +query-engine:" -A8 | awk '/^ +image:/ {print $2}')

docker run --rm --name query-engine \
	--network host \
	-v /opt/repos:/opt/repos \
	-e PYTHONPATH=/opt/repos \
	-e DAS_MONGODB_NAME \
	-e DAS_MONGODB_HOSTNAME \
	-e DAS_MONGODB_PORT \
	-e DAS_REDIS_HOSTNAME \
	-e DAS_REDIS_PORT \
	-e DAS_MONGODB_USERNAME \
	-e DAS_MONGODB_PASSWORD \
	$FUNCTION_NAME

#tail -f /dev/null
