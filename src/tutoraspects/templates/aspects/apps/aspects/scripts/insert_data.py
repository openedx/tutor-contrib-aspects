import clickhouse_connect
import json
import glob
import sys
import os

DBT_PROJECT_ROOT = "/app/aspects-dbt"

DBT_STATE_DIR = "{{DBT_STATE_DIR}}"
print("Insert data script.")
client = clickhouse_connect.get_client(
    host="{{CLICKHOUSE_HOST}}",
    username='{{CLICKHOUSE_ADMIN_USER}}',
    password='{{CLICKHOUSE_ADMIN_PASSWORD}}',
    port={{ CLICKHOUSE_INTERNAL_HTTP_PORT }},
    secure={{ CLICKHOUSE_SECURE_CONNECTION }}
)

def sink_files():
    files = []
    file_name = f"{DBT_STATE_DIR}/manifest.json"

    with open(file_name, "r") as file:
        content = file.read()
        name = file_name.split("/")[-1]
        print(f"Sinking file: {name}")
        files.append({
            "path": name,
            "content": content
        })



    client.query(
    f"""
    INSERT INTO {{ ASPECTS_EVENT_SINK_DATABASE }}.aspects_data FORMAT JSONEachRow {json.dumps(files)}
    """
    )

def load_files():
    result = client.query("SELECT path, content from {{ ASPECTS_EVENT_SINK_DATABASE }}.aspects_data OPTIMIZE FINAL")
    if not result.result_rows:
        print("There is no state stored.")
    for row in result.result_rows:
        path, content = row
        if path == "manifest.json":
            file_path = f"{DBT_STATE_DIR}/manifest.json"
        if path == "superset_exposures.yaml":
            file_path = f"models/{path}"
        with open(file_path, "w") as f:
            print(f"Loading: {file_path}")
            f.write(content)


if __name__ == '__main__':
    if sys.argv[1] == "sink":
        sink_files()
    if sys.argv[1] == "load":
        load_files()
