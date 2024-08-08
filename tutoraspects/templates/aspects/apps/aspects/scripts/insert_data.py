import clickhouse_connect
import os
import json
import glob

client = clickhouse_connect.get_client(
    host="{{CLICKHOUSE_HOST}}",
    username='{{CLICKHOUSE_ADMIN_USER}}',
    password='{{CLICKHOUSE_ADMIN_PASSWORD}}'
)

for file_name in glob.iglob(ASSETS_PATH + "/**/*.yaml", recursive=True):
    with open(file_name, "r", encoding="utf-8") as file:
        # We have to remove the jinja for it to parse
        file_str = file.read()

with open(file_path) as f:
    file_content = json.load(f)
    content = json.dumps({"path": file_path, "content": file_content})
    client.raw_query(
    f"""
    CREATE TABLE if not exists test(
        path String,
        content String
    ) ENGINE Memory
    """
    )
    client.raw_query(
    f"""
    INSERT INTO test FORMAT JSONEachRow {content}
    """
    )
