cd /app/oars/clickhouse/migrations
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
alembic upgrade head
