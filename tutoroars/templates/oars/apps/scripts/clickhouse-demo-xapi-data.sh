#!/usr/bin/env bash

python3 -m venv virtualenv
. virtualenv/bin/activate

echo "Loading demo xAPI data..."
pip install git+https://github.com/openedx/xapi-db-load@0.1#egg=xapi-db-load==0.1
pip install pandas  # clickhouse_connect is missing this
xapi-db-load --backend ralph_clickhouse \
    --num_batches $1 \
    --batch_size $2 \
    --db_host "{{ CLICKHOUSE_HOST }}" \
    --db_port "{{ CLICKHOUSE_HTTP_PORT }}" \
    --db_username "{{ CLICKHOUSE_ADMIN_USER }}" \
    --db_password "{{ CLICKHOUSE_ADMIN_PASSWORD }}" \
    --db_name "{{ OARS_XAPI_DATABASE }}" \
    --lrs_url "http://ralph:{{ RALPH_PORT }}/xAPI/statements/" \
    --lrs_username "{{RALPH_LMS_USERNAME}}" \
    --lrs_password "{{RALPH_LMS_PASSWORD}}"

echo "Done."
