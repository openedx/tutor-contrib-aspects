from superset.app import create_app

app = create_app()
app.app_context().push()


import json
import logging
import time
import uuid
from datetime import datetime
from unittest.mock import patch

import sqlparse
from flask import g
from superset import security_manager
from superset.charts.data.commands.get_data_command import ChartDataCommand
from superset.charts.schemas import ChartDataQueryContextSchema
from superset.extensions import db
from superset.models.dashboard import Dashboard
from superset.models.slice import Slice

logger = logging.getLogger("performance_metrics")

ASPECTS_VERSION = "{{ASPECTS_VERSION}}"
UUID = str(uuid.uuid4())[0:6]
RUN_ID = f"aspects-{ASPECTS_VERSION}-{UUID}"

report_format = "{i}. {slice}\n" "Superset time: {superset_time} (s).\n"

query_format = (
    "Query duration: {query_duration_ms} (s).\n"
    "Result rows: {result_rows}\n"
    "Memory Usage (MB): {memory_usage_mb}\n"
    "Row count (superset) {rowcount:}\n"
    "Filters: {filters}\n\n"
)


def performance_metrics():
    """Measure the performance of the dashboard."""
    # Mock the client name to identify the queries in the clickhouse system.query_log table by
    # by the http_user_agent field.
    with patch("clickhouse_connect.common.build_client_name") as mock_build_client_name:
        mock_build_client_name.return_value = RUN_ID
        embedable_dashboards = {{SUPERSET_EMBEDDABLE_DASHBOARDS}}
        dashboards = (
            db.session.query(Dashboard)
            .filter(Dashboard.slug.in_(embedable_dashboards))
            .all()
        )
        report = []
        for dashboard in dashboards:
            logger.info(f"Dashboard: {dashboard.slug}")
            for slice in dashboard.slices:
                result = measure_chart(slice)
                for query in result["queries"]:
                    # Remove the data from the query to avoid memory issues on large datasets.
                    query.pop("data")
                report.append(result)
        return report


def measure_chart(slice, extra_filters=[]):
    """
    Measure the performance of a chart and return the results.
    """
    logger.info(f"Fetching slice data: {slice}")
    query_context = json.loads(slice.query_context)
    query_context.update(
        {
            "result_format": "json",
            "result_type": "full",
            "force": True,
            "datasource": {
                "type": "table",
                "id": slice.datasource_id,
            },
        }
    )

    if extra_filters:
        query_context["filters"].extend(extra_filters)

    g.user = security_manager.find_user(username="{{SUPERSET_ADMIN_USERNAME}}")
    query_context = ChartDataQueryContextSchema().load(query_context)
    command = ChartDataCommand(query_context)

    start_time = datetime.now()
    result = command.run()
    end_time = datetime.now()

    result["time_elapsed"] = (end_time - start_time).total_seconds()
    result["slice"] = slice
    return result


def get_query_log_from_clickhouse(report):
    """
    Get the query log from clickhouse and print the results.
    """
    chart_uuid = "bb13bb31-c797-4ed3-a7f9-7825cc6dc482"

    slice = db.session.query(Slice).filter(Slice.uuid == chart_uuid).one()

    query_context = json.loads(slice.query_context)
    query_context["queries"][0]["filters"].append(
        {"col": "http_user_agent", "op": "==", "val": RUN_ID}
    )
    slice.query_context = json.dumps(query_context)

    result = measure_chart(slice)

    clickhouse_queries = {}
    for query in result["queries"]:
        for row in query["data"]:
            parsed_sql = str(sqlparse.parse(row.pop("query"))[0])
            clickhouse_queries[parsed_sql] = row

    # Sort report by slowest queries
    report = sorted(report, key=lambda x: x["time_elapsed"], reverse=True)

    report_str = f"\nSuperset Reports: {RUN_ID}\n\n"
    for i, result in enumerate(report):
        report_str+=(
            report_format.format(
                i=(i + 1), slice=result["slice"], superset_time=result["time_elapsed"]
            )
        )
        for i, query in enumerate(result["queries"]):
            parsed_sql = (
                str(sqlparse.parse(query["query"])[0]).replace(";", "")
                + "\n FORMAT Native"
            )
            clickhouse_report = clickhouse_queries.get(parsed_sql, {})
            report_str+=(
                query_format.format(
                    query_duration_ms=clickhouse_report.get("query_duration_ms") / 1000,
                    memory_usage_mb=clickhouse_report.get("memory_usage_mb"),
                    result_rows=clickhouse_report.get("result_rows"),
                    rowcount=query["rowcount"],
                    filters=query["applied_filters"],
                )
            )
    logger.info(report_str)


if __name__ == "__main__":
    logger.info(f"Running performance metrics. RUN ID: {RUN_ID}")
    report = performance_metrics()
    # Clickhouse query log takes some seconds to log queries.
    logger.info("Waiting for clickhouse log...")
    time.sleep(10)
    get_query_log_from_clickhouse(report)
