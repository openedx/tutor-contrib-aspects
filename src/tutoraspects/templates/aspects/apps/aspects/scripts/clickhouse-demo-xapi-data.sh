#!/usr/bin/env bash
echo "Loading demo xAPI data..."
cat $1
xapi-db-load load-db --config_file $1 || { ec=$?; printf '%s\n' "Error loading demo data!" >&2; exit $ec; }

echo "Done."
