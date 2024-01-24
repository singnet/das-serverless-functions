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

docker run --name query-engine \
	--network host \
	--env-file .env \
	-v /opt/repos:/opt/repos \
	trueagi/das:v1.5.0-queryengine

#tail -f /dev/null
