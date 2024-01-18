#!/usr/bin/env bash
echo "Loading demo xAPI data..."
xapi-db-load load-db --config_file $1

echo "Done."
