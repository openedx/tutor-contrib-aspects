FROM python:3.12

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.10.8 /uv /uvx /bin/
ENV PATH="/root/.local/bin/:$PATH"
COPY ./requirements.txt /app/requirements.txt

RUN uv pip install -r /app/requirements.txt --system
RUN git clone --depth 1 -b {{ DBT_BRANCH }} {{ DBT_REPOSITORY }} aspects-dbt

WORKDIR /app/aspects-dbt
RUN uv pip install -r requirements.txt --system
RUN dbt deps

WORKDIR /app
