"""Aspects module for tutor v1 commands"""

from __future__ import annotations

import string
import sys

import click
from tutor import env

from tutoraspects.asset_command_helpers import (
    ASSETS_PATH,
    SupersetCommandError,
    deduplicate_superset_assets,
    import_superset_assets,
    delete_aspects_unused_assets,
    find_unused_queries,
)


@click.command()
@click.option("-c", "--config_file", default="./xapi-db-load-config.yaml")
def load_xapi_test_data(config_file) -> list[tuple[str, str]]:
    """
    Job that loads bogus test xAPI data to ClickHouse via Ralph.
    """
    return [
        (
            "aspects",
            f"echo 'Running script... {config_file}' && "
            "cd /app/aspects/scripts/ && "
            f"bash clickhouse-demo-xapi-data.sh {config_file} && "
            "echo 'Done!';",
        ),
    ]


# Ex: "tutor local do dbt "
@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-c",
    "--command",
    default="run",
    type=click.UNPROCESSED,
    help="""The full dbt command to run configured ClickHouse database, wrapped in
         double quotes. The list of commands can be found in the CLI section here:
         https://docs.getdbt.com/reference/dbt-commands

         Examples:

         tutor local do dbt -c "test"

         tutor local do dbt -c "run -m enrollments_by_day --threads 4"
         """,
)
@click.option(
    "--only_changed",
    default=True,
    type=click.UNPROCESSED,
    help="""Whether to only run models that have changed since the last dbt run. Since
         re-running materialized views will recreate potentially huge datasets and
         incur downtime, this defaults to true.

         If no prior state is found, the command will run as if this was False.

         If your command fails due to an issue with "state:modified", you may need to
         set this to False.
         """,
)
def dbt(only_changed: bool, command: string) -> list[tuple[str, str]]:
    """
    Job that proxies dbt commands to a container which runs them against ClickHouse.
    """
    return [
        (
            "aspects",
            "echo 'Making dbt script executable...' && "
            f"echo 'Running dbt, only_changed: {only_changed} command: {command}' && "
            f"bash /app/aspects/scripts/dbt.sh {only_changed} {command} && "
            "echo 'Done!';",
        ),
    ]


# Ex: "tutor local do alembic "
@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "-c",
    "--command",
    default="run",
    type=click.UNPROCESSED,
    help="""The full alembic command to run configured ClickHouse database, wrapped in
            double quotes. The list of commands can be found in the CLI section here:
            https://alembic.sqlalchemy.org/en/latest/cli.html#command-reference
            Examples:

            tutor local do alembic -c "current" # Show current revision
            tutor local do alembic -c "history" # Show revision history
            tutor local do alembic -c "revision --autogenerate -m 'Add new table'" # Create new revision
            tutor local do alembic -c "upgrade head" # Upgrade to latest migrations
            tutor local do alembic -c "downgrade base" # Downgrade to base migration
         """,
)
def alembic(command: string) -> list[tuple[str, str]]:
    """
    Job that proxies alembic commands to a container which runs them against ClickHouse.
    """
    return [
        (
            "aspects",
            "echo 'Making dbt script executable...' && "
            f"bash /app/aspects/scripts/alembic.sh {command} && "
            "echo 'Done!';",
        ),
    ]


# Ex: "tutor local do import-assets "
@click.command(context_settings={"ignore_unknown_options": True})
def import_assets() -> list[tuple[str, str]]:
    """
    Job to import Superset assets.
    """
    return [
        (
            "superset",
            "echo 'Importing assets...' && "
            "bash /app/scripts/import-assets.sh && "
            "echo 'Done!';",
        ),
    ]


@click.command(context_settings={"ignore_unknown_options": True})
def init_clickhouse() -> list[tuple[str, str]]:
    """
    Job to run ClickHouse initialization tasks.
    """
    return [
        (
            "clickhouse",
            env.read_template_file(
                "aspects", "jobs", "init", "clickhouse", "init-clickhouse.sh"
            ),
        )
    ]


# Ex: "tutor local do performance-metrics "
@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "--org",
    default="",
    help="An organization to apply as a filter.",
)
@click.option(
    "--course_name",
    default="",
    help="A course_name to apply as a filter.",
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
    "--print_sql", is_flag=True, default=False, help="Print the SQL that was run."
)
@click.option(
    "--fail_on_error", is_flag=True, default=False, help="Allow errors to fail the run."
)
def performance_metrics(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    org, course_name, dashboard_slug, slice_name, print_sql, fail_on_error
) -> (list)[tuple[str, str]]:
    """
    Job to measure performance metrics of charts and its queries in Superset and ClickHouse.
    """
    options = ""
    options += f"--org '{org}' " if org else ""
    options += f"--course_name '{course_name}' " if course_name else ""
    options += f" --dashboard_slug {dashboard_slug}" if dashboard_slug else ""
    options += f' --slice_name "{slice_name}"' if slice_name else ""
    options += " --print_sql" if print_sql else ""
    options += " --fail_on_error" if fail_on_error else ""

    return [
        (
            "superset",
            "set -e && "
            "echo 'Performance...' && "
            f"python /app/pythonpath/performance_metrics.py {options} &&"
            "echo 'Done!';",
        ),
    ]


# Ex: "tutor local do collect-dbt-lineage"
@click.command(context_settings={"ignore_unknown_options": True})
def collect_dbt_lineage() -> (list)[tuple[str, str]]:
    """
    Job to dump a list of dbt resources used in Superset.

    aspects-dbt uses this to update the list of exposures so we can identify which
    models are being used, and where.
    """
    return [
        (
            "superset",
            "set -e && "
            "echo 'Collecting dbt lineage...' && "
            "python /app/pythonpath/collect_dbt_lineage.py &&"
            "echo 'Done!';",
        ),
    ]


# Ex: "tutor local do dump_data_to_clickhouse "
@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "--service",
    default="lms",
    type=click.UNPROCESSED,
    help="The service to run the command on.",
)
@click.option("--options", default="", type=click.UNPROCESSED)
def dump_data_to_clickhouse(service, options) -> list[tuple[str, str]]:
    """
    Job that proxies the dump_data_to_clickhouse commands.
    """
    return [(f"{service}", f"./manage.py {service} dump_data_to_clickhouse {options}")]


# pylint: disable=line-too-long
# Ex: tutor local do transform-tracking-logs --options "--source_provider LOCAL --source_config '{\"key\": \"/openedx/data/\", \"prefix\": \"tracking.log\", \"container\": \"logs\"}' --destination_provider LRS --transformer_type xapi"
# Ex: tutor local do transform-tracking-logs --options "--source_provider MINIO --source_config '{\"key\": \"openedx\", \"secret\": \"h3SIhXAqDDxJAP6TcXklNxro\", \"container\": \"openedx\", \"prefix\": \"/tracking_logs\", \"host\": \"files.local.overhang.io\", \"secure\": false}' --destination_provider LRS --transformer_type xapi"
@click.command(context_settings={"ignore_unknown_options": True})
@click.option(
    "--source_provider",
    type=str,
    required=True,
    help="An Apache Libcloud provider. This is mandatory.",
)
@click.option(
    "--source_config",
    type=str,
    required=True,
    help="A JSON dictionary of configuration for the source provider. This is mandatory.",
)
@click.option(
    "--destination_provider",
    type=str,
    default="LRS",
    help="Either 'LRS' or an Apache Libcloud provider. The default is 'LRS'.",
)
@click.option(
    "--destination_config",
    type=str,
    help=(
        "A JSON dictionary of configuration for the destination provider. "
        "Optional if 'LRS' is used as the destination_provider."
    ),
)
@click.option(
    "--transformer_type",
    type=click.Choice(["xapi", "caliper"]),
    required=True,
    help="The type of transformation to perform, either 'xapi' or 'caliper'. This is mandatory.",
)
@click.option(
    "--batch_size",
    type=int,
    default=10000,
    help="The batch size. The default is 10000.",
)
@click.option(
    "--sleep_between_batches_secs",
    type=float,
    default=10.0,
    help="The amount of time (in seconds) to sleep between sending batches. Default is 10.0 seconds.",
)
@click.option(
    "--dry_run",
    is_flag=True,
    help=(
        "A flag to determine if this is a dry run. If present, all lines from all files "
        "will be attempted to be transformed, but won't be sent to the destination."
    ),
)
@click.option(
    "--deduplicate",
    is_flag=True,
    help=(
        "This should only be added if you believe events will be duplicated such as replaying logs"
        "that have already been added. De-duplication can take a very long time to process."
    ),
)
def transform_tracking_logs(deduplicate, **kwargs) -> list[tuple[str, str]]:
    """
    Job that proxies the transform_tracking_logs commands.
    """

    options = []
    for arg, value in kwargs.items():
        if not value:
            continue
        if arg == "dry_run":
            options.append(f"--{arg}")
        elif arg in ("source_config", "destination_config"):
            options.append(f"--{arg} '{value}'")
        else:
            options.append(f"--{arg} {value}")

    options_str = " ".join(options)

    command = f"./manage.py lms transform_tracking_logs {options_str}"

    tasks = [
        ("lms", command),
    ]

    if deduplicate:
        tasks.append(
            (
                "clickhouse",
                env.read_template_file(
                    "aspects", "jobs", "init", "clickhouse", "deduplicate.sh"
                ),
            )
        )

    return tasks


@click.group()
def aspects() -> None:
    """
    Custom commands for the Aspects plugin.
    """


@aspects.command("import_superset_zip")
@click.option(
    "--base_assets_path",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, readable=True, writable=True
    ),
    default=ASSETS_PATH,
    help="Path where you want the assets imported to. This is only necessary when importing assets to an Aspects extension. If you are updating Aspects itself you can leave the default.",
)
@click.argument("file", type=click.File("r"))
def serialize_zip(file, base_assets_path):
    """
    Script that serializes a zip file to the assets.yaml file.
    """
    try:
        import_superset_assets(file, click.echo, base_assets_path)
    except SupersetCommandError:
        click.echo()
        click.echo("Errors found on import. Please correct the issues, then run:")
        click.echo(click.style("tutor aspects check_superset_assets", fg="green"))
        sys.exit(-1)

    click.echo()
    deduplicate_superset_assets(click.echo)
    delete_aspects_unused_assets(click.echo)
    find_unused_queries(click.echo)

    click.echo()
    click.echo("Asset merge complete!")
    click.echo()
    click.echo(
        click.style(
            "PLEASE check your diffs for exported passwords before committing!",
            fg="yellow",
        )
    )


@aspects.command("check_superset_assets")
def check_superset_assets():
    """
    Deduplicate assets by UUID, and check for duplicate asset names.
    """
    deduplicate_superset_assets(click.echo)
    delete_aspects_unused_assets(click.echo)
    find_unused_queries(click.echo)

    click.echo()
    click.echo(
        click.style(
            "PLEASE check your diffs for exported passwords before committing!",
            fg="yellow",
        )
    )


DO_COMMANDS = (
    load_xapi_test_data,
    dbt,
    alembic,
    dump_data_to_clickhouse,
    transform_tracking_logs,
    import_assets,
    performance_metrics,
    init_clickhouse,
    collect_dbt_lineage,
)

COMMANDS = (aspects,)
