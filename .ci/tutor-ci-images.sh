#!/usr/bin/env bash
# Point Tutor at this repository's GitHub Container Registry namespace for the
# images that the integration tests build.
#
# Tutor reads any config key from a TUTOR_<KEY> environment variable, so
# exporting these overrides every later `tutor` invocation without touching
# .ci/config.yml. When running under GitHub Actions the variables are appended
# to $GITHUB_ENV so they apply to every subsequent step of the job.
#
# The images themselves are never pushed: only the BuildKit layer cache is.
# `tutor images build` always reads from <image>-cache, so with these names in
# place every build pulls cached layers from ghcr.io and only rebuilds layers
# whose inputs changed on the branch under test. build-ci-cache.yaml refreshes
# the cache from main.
#
# Usage: .ci/tutor-ci-images.sh ghcr.io/<owner>/<repo> [tag]
set -euo pipefail

REGISTRY_PREFIX="${1:?usage: $0 ghcr.io/<owner>/<repo> [tag]}"
REGISTRY_PREFIX="${REGISTRY_PREFIX,,}"   # GHCR requires lowercase names
TAG="${2:-ci}"

# Tutor image name -> config key -> ghcr.io repository name (mirrors the
# edunext/* names in .ci/config.yml and tutoraspects/plugin.py).
declare -A IMAGE_KEYS=(
  [openedx]=DOCKER_IMAGE_OPENEDX
  [openedx-dev]=DOCKER_IMAGE_OPENEDX_DEV
  [aspects]=DOCKER_IMAGE_ASPECTS
  [aspects-superset]=DOCKER_IMAGE_SUPERSET
)
declare -A IMAGE_NAMES=(
  [openedx]=openedx-aspects
  [openedx-dev]=openedx-aspects-dev
  [aspects]=aspects
  [aspects-superset]=aspects-superset
)

# Emit in a stable order so logs are easy to read.
ASPECTS_CI_IMAGES="openedx openedx-dev aspects aspects-superset"

emit() {
  echo "$1"
  if [ -n "${GITHUB_ENV:-}" ]; then
    echo "$1" >> "$GITHUB_ENV"
  fi
}

for image in $ASPECTS_CI_IMAGES; do
  emit "TUTOR_${IMAGE_KEYS[$image]}=${REGISTRY_PREFIX}/${IMAGE_NAMES[$image]}:${TAG}"
done
# Space-separated list of the Tutor image names above, for
# `tutor images build $ASPECTS_CI_IMAGES --cache-to-registry`.
emit "ASPECTS_CI_IMAGES=${ASPECTS_CI_IMAGES}"
