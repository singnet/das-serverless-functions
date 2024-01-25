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
	--env-file .env \
	-v /opt/repos:/opt/repos \
	-e PYTHONPATH=/opt/repos \
	$FUNCTION_NAME

#tail -f /dev/null
