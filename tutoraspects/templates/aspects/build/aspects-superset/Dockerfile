# Superset image with additional database drivers
# https://hub.docker.com/r/apache/superset
# https://github.com/apache/superset/releases
# https://github.com/apache/superset/blob/master/Dockerfile
# https://superset.apache.org/docs/databases/installing-database-drivers
FROM apache/superset:2.0.1

USER root

COPY ./requirements.txt /app/requirements.txt

RUN \
    {% if is_buildkit_enabled() %}--mount=type=cache,target=/var/cache/apt \{% endif %}
    apt-get update && apt-get install -y zip

RUN \
    {% if is_buildkit_enabled() %}--mount=type=cache,target=/root/.cache/pip,sharing=shared \{% endif %}
    pip install -r /app/requirements.txt
