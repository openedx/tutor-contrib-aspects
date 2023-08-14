"""Aspects module for tutor v1 commands"""
from __future__ import annotations

import string

import click


@click.command()
@click.option("-n", "--num_batches", default=100)
@click.option("-s", "--batch_size", default=100)
def load_xapi_test_data(num_batches: int, batch_size: int) -> list[tuple[str, str]]:
    """
    Job that loads bogus test xAPI data to ClickHouse via Ralph.
    """
    return [
        (
            "aspects",
            "echo 'Making demo xapi script executable...' && "
            "echo 'Done. Running script...' && "
            f"bash /app/aspects/scripts/clickhouse-demo-xapi-data.sh {num_batches}"
            f" {batch_size} && "
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
def dbt(command: string) -> list[tuple[str, str]]:
    """
    Job that proxies dbt commands to a container which runs them against ClickHouse.
    """
    return [
        (
            "aspects",
            "echo 'Making dbt script executable...' && "
            f"echo 'Running dbt {command}' && "
            f"bash /app/aspects/scripts/dbt.sh {command} && "
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


# Ex: "tutor local do dump_courses_to_clickhouse "
@click.command(context_settings={"ignore_unknown_options": True})
@click.option("--options", default="", type=click.UNPROCESSED)
def dump_courses_to_clickhouse(options) -> list[tuple[str, str]]:
    """
    Job that proxies the dump_courses_to_clickhouse commands.
    """
    return [("cms", f"./manage.py cms dump_courses_to_clickhouse {options}")]


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
def transform_tracking_logs(**kwargs) -> list[tuple[str, str]]:
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

    return [("lms", command)]


COMMANDS = (
    load_xapi_test_data,
    dbt,
    alembic,
    dump_courses_to_clickhouse,
    transform_tracking_logs,
)
