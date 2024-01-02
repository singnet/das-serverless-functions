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

faas-cli local-run --network host --watch
#tail -f /dev/null
