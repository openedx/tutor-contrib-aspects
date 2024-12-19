"""
Gather performance metrics on Superset chart queries.

Reads the queries from the superset database, and enriches them with the
query_context from the asset files. The query_context cannot be stored in the
database on import due to is using database primary keys which do not match
across Superset installations.
"""

import logging
import os
import time
import uuid
from datetime import datetime
from unittest.mock import patch

import click
import sqlparse
import yaml
from create_assets import app

from flask import g
from superset import security_manager
from superset.charts.schemas import ChartDataQueryContextSchema
from superset.commands.chart.data.get_data_command import ChartDataCommand
from superset.extensions import db
from superset.models.dashboard import Dashboard
from superset.models.slice import Slice

logger = logging.getLogger("performance_metrics")

ASPECTS_VERSION = "{{ASPECTS_VERSION}}"
UUID = str(uuid.uuid4())[0:6]
RUN_ID = f"aspects-{ASPECTS_VERSION}-{UUID}"
CHART_PATH = "/app/openedx-assets/assets/charts/"
DASHBOARDS = {{SUPERSET_EMBEDDABLE_DASHBOARDS}}
DASHBOARDS.update({{SUPERSET_DASHBOARDS}})

report_format = "{i}. {dashboard} - {slice}\n" "Superset time: {superset_time} (s).\n"

query_format = (
    "Query duration: {query_duration_ms} (s).\n"
    "Result rows: {result_rows}\n"
    "Memory Usage (MB): {memory_usage_mb}\n"
    "Row count (superset) {rowcount:}\n"
    "Filters: {filters}\n"
    "SQL:\n"
    "{sql}\n\n\n"
)


@click.command()
@click.option("--org", default="", help="An organization to apply as a filter.")
@click.option(
    "--course_name",
    default="",
    help="A course_name to apply as a filter, you must include the 'course-v1:'.",
)
@click.option(
    "--dashboard_slug", default="", help="Only run charts for the given dashboard."
)
@click.option(
    "--slice_name",
    default="",
    help="Only run charts for the given slice name, if the name appears in more than "
    "one dashboard it will be run for each.",
)
@click.option(
    "--print_sql", is_flag=True, default=False, help="Whether to print the SQL run."
)
@click.option(
    "--fail_on_error", is_flag=True, default=False, help="Allow errors to fail the run."
)
def performance_metrics(
    org, course_name, dashboard_slug, slice_name, print_sql, fail_on_error
):
    """
    Measure the performance of the dashboard.
    """
    # Mock the client name to identify the queries in the clickhouse system.query_log
    # table by by the http_user_agent field.
    extra_filters = []
    if course_name:
        extra_filters += [{"col": "course_name", "op": "IN", "val": course_name}]
    if org:
        extra_filters += [{"col": "org", "op": "IN", "val": org}]

    chart_count = 0
    with patch("clickhouse_connect.common.build_client_name") as mock_build_client_name:
        mock_build_client_name.return_value = RUN_ID
        target_dashboards = (
            [dashboard_slug] if dashboard_slug else DASHBOARDS
        )

        dashboards = (
            db.session.query(Dashboard)
            .filter(Dashboard.slug.in_(target_dashboards))
            .all()
        )
        report = []

        if not dashboards:
            logger.warning(f"No dashboard found for {target_dashboards}")

        query_contexts = get_query_contexts_from_assets()
        for dashboard in dashboards:
            logger.info(f"Dashboard: {dashboard.slug}")
            for slice in dashboard.slices:
                if slice_name and not slice_name == slice.slice_name:
                    logger.info(
                        f"{slice.slice_name} doesn't match {slice_name}, " f"skipping."
                    )
                    continue

                query_context = get_slice_query_context(
                    slice, query_contexts, extra_filters
                )
                result = measure_chart(slice, query_context, fail_on_error)
                if not result:
                    continue
                chart_count += 1
                for query in result["queries"]:
                    # Remove the data from the query to avoid memory issues on large
                    # datasets.
                    query.pop("data")

                result["dashboard"] = dashboard.slug
                report.append(result)

        if not report:
            logger.warning("No target charts found!")
            return report

        get_query_log_from_clickhouse(report, query_contexts, print_sql, fail_on_error, chart_count)
        return report


def get_query_contexts_from_assets():
    query_contexts = {}

    for root, dirs, files in os.walk(CHART_PATH):
        for file in files:
            if not file.endswith(".yaml"):
                continue

            path = os.path.join(root, file)
            with open(path, "r") as file:
                asset = yaml.safe_load(file)
                if "query_context" in asset and asset["query_context"]:
                    query_contexts[asset["uuid"]] = asset["query_context"]

    logger.info(f"Found {len(query_contexts)} query contexts")
    return query_contexts


def get_slice_query_context(slice, query_contexts, extra_filters=None):
    if not extra_filters:
        extra_filters = []

    query_context = query_contexts.get(str(slice.uuid), {})
    if not query_context:
        logger.info(f"SLICE {slice} has no query context! {slice.uuid}")
        logger.info(query_contexts.keys())

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

    query_context["form_data"]["extra_form_data"] = {"filters": extra_filters}

    if extra_filters:
        for query in query_context["queries"]:
            query["filters"] += extra_filters

    return query_context


def measure_chart(slice, query_context_dict, fail_on_error):
    """
    Measure the performance of a chart and return the results.
    """
    logger.info(f"Fetching slice data: {slice} {slice.uuid}")

    g.user = security_manager.find_user(username="{{SUPERSET_ADMIN_USERNAME}}")
    query_context = ChartDataQueryContextSchema().load(query_context_dict)
    command = ChartDataCommand(query_context)
    command.validate()
    g.form_data = query_context.form_data
    try:
        start_time = datetime.now()
        result = command.run()
        end_time = datetime.now()
        result["time_elapsed"] = (end_time - start_time).total_seconds()
        result["slice"] = slice
        result["uuid"] = slice.uuid
        for query in result["queries"]:
            if "error" in query and query["error"]:
                raise query["error"]
    except Exception as e:
        logger.error(f"Error fetching slice data: {slice}. Error: {e}")
        if fail_on_error:
            raise e
        return

    return result


def get_query_log_from_clickhouse(report, query_contexts, print_sql, fail_on_error, chart_count):
    """
    Get the query log from clickhouse and print the results.
    """
    # This corresponds to the "Query Performance" chart in Superset
    chart_uuid = "bb13bb31-c797-4ed3-a7f9-7825cc6dc482"

    slice = db.session.query(Slice).filter(Slice.uuid == chart_uuid).one()

    query_context = get_slice_query_context(slice, query_contexts)
    query_context["queries"][0]["filters"].append(
        {"col": "http_user_agent", "op": "==", "val": RUN_ID}
    )

    ch_chart_result = measure_chart(slice, query_context, fail_on_error)

    # Run CH query until results for all slices are returned
    ch_count = 6
    while ch_count > 0:
        missing_rows = chart_count - ch_chart_result["queries"][0]["rowcount"]
        if missing_rows > 0:
            logger.info(f"Waiting for {missing_rows} clickhouse logs...")
            time.sleep(5)
            ch_chart_result = measure_chart(slice, query_context, fail_on_error)
            ch_count -= 1
        else:
            break

    clickhouse_queries = {}
    for query in ch_chart_result["queries"]:
        for row in query["data"]:
            parsed_sql = str(sqlparse.parse(row.pop("query"))[0])
            clickhouse_queries[parsed_sql] = row

    for k, chart_result in enumerate(report):
        for query in chart_result["queries"]:
            parsed_sql = (
                str(sqlparse.parse(query["query"].strip())[0]).replace(";", "")
                + "\n FORMAT Native"
            )
            chart_result["sql"] = parsed_sql
            clickhouse_report = clickhouse_queries.get(parsed_sql, {})
            chart_result.update(clickhouse_report)
            chart_result.update(
                {"query_duration_ms": chart_result.get("query_duration_ms", 0)}
            )

    # Sort report by slowest queries
    report = sorted(report, key=lambda x: x["query_duration_ms"], reverse=True)

    report_str = f"\nSuperset Reports: {RUN_ID}\n\n"
    for k, chart_result in enumerate(report):
        report_str += report_format.format(
            i=(k + 1),
            dashboard=chart_result["dashboard"],
            slice=f'{chart_result["slice"]} {chart_result["uuid"]}',
            superset_time=chart_result["time_elapsed"],
        )
        for query in chart_result["queries"]:
            report_str += query_format.format(
                query_duration_ms=chart_result.get("query_duration_ms") / 1000,
                memory_usage_mb=chart_result.get("memory_usage_mb"),
                result_rows=chart_result.get("result_rows"),
                rowcount=query["rowcount"],
                filters=query["applied_filters"],
                sql=chart_result["sql"] if print_sql else "",
            )
    logger.info(report_str)


if __name__ == "__main__":
    logger.info(f"Running performance metrics. RUN ID: {RUN_ID}")
    performance_metrics()
