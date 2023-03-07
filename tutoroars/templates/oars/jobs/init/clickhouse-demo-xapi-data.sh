#!/usr/bin/env bash

case "{{ CLICKHOUSE_LOAD_DEMO_DATA }}" in

    *"xapi"*)
        python3 -m venv virtualenv
        . virtualenv/bin/activate

        echo "Loading demo xAPI data..."
        pip install git+https://github.com/openedx/xapi-db-load@0.1#egg=xapi-db-load==0.1
        pip install pandas  # clickhouse_connect is missing this
        xapi-db-load --backend clickhouse \
            --num_batches "{{ CLICKHOUSE_LOAD_DEMO_XAPI_BATCHES }}" \
            --batch_size "{{ CLICKHOUSE_LOAD_DEMO_XAPI_BATCH_SIZE }}" \
            --db_host "{{ CLICKHOUSE_HOST }}" \
            --db_port "{{ CLICKHOUSE_HTTP_PORT }}" \
            --db_username "{{ CLICKHOUSE_ADMIN_USER }}" \
            --db_password "{{ CLICKHOUSE_ADMIN_PASSWORD }}" \
            --db_name "{{ CLICKHOUSE_XAPI_DATABASE }}"
        echo "Done."
        ;;
esac
