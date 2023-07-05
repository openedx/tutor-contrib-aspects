#!/usr/bin/env bash
echo "Loading demo xAPI data..."
xapi-db-load --backend ralph_clickhouse \
    --num_batches $1 \
    --batch_size $2 \
    --db_host "{{ CLICKHOUSE_HOST }}" \
    --db_port "{{ CLICKHOUSE_PORT }}" \
    --db_username "{{ CLICKHOUSE_ADMIN_USER }}" \
    --db_password "{{ CLICKHOUSE_ADMIN_PASSWORD }}" \
    --db_name "{{ ASPECTS_XAPI_DATABASE }}" \
    --lrs_url "{% if RUN_RALPH %}http://ralph:{{ RALPH_PORT }}{% else %}{% if RALPH_RUN_HTTPS %}https://{% else %}http://{% endif %}{{ RALPH_HOST }}{% endif %}/xAPI/statements/" \
    --lrs_username "{{RALPH_LMS_USERNAME}}" \
    --lrs_password "{{RALPH_LMS_PASSWORD}}"

echo "Done."
