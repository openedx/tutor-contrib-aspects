FROM python:3.12

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

RUN git clone -b {{ DBT_BRANCH }} {{ DBT_REPOSITORY }} aspects-dbt

RUN pip install -r /app/aspects-dbt/requirements.txt
