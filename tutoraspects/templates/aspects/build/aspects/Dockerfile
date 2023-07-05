FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY *.sh .

RUN \
    {% if is_buildkit_enabled() %}--mount=type=cache,target=/root/.cache/pip,sharing=shared \{% endif %}
    pip install -r /app/requirements.txt

