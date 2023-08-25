"""Aspects module for tutor v0 commands"""
import click
from tutor import config as tutor_config

from tutor import env


@click.command(help="Run dbt with the provided command and options.")
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
@click.pass_obj
def dbt(context, command) -> None:
    """
    Job that proxies dbt commands to a container which runs them against ClickHouse.
    """
    config = tutor_config.load(context.root)
    runner = context.job_runner(config)

    command = f"""echo 'Making dbt script executable...'
    echo 'Running dbt {command}' 
    bash /app/aspects/scripts/dbt.sh {command}
    echo 'Done!';
    """
    runner.run_job("aspects", command)


@click.command(help="Load generated fake xAPI test data to ClickHouse.")
@click.option("-n", "--num_batches", default=100)
@click.option("-s", "--batch_size", default=100)
@click.pass_obj
def load_xapi_test_data(context, num_batches, batch_size) -> None:
    """
    Job that loads bogus test xAPI data to ClickHouse via Ralph.
    """
    config = tutor_config.load(context.root)
    runner = context.job_runner(config)

    command = f"""echo 'Making demo xapi script executable...'
    echo 'Done. Running script...'
    bash /app/aspects/scripts/clickhouse-demo-xapi-data.sh {num_batches} {batch_size}
    echo 'Done!';
    """
    runner.run_job("aspects", command)


@click.command(
    help="Run Alembic migrations with the given options.",
    context_settings={"ignore_unknown_options": True},
)
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
@click.pass_obj
def alembic(context, command) -> None:
    """
    Job that proxies alembic commands to a container which runs them against ClickHouse.
    """
    config = tutor_config.load(context.root)
    runner = context.job_runner(config)

    command = f"""echo 'Making demo xapi script executable...'
    echo 'Done. Running script...'
    bash /app/aspects/scripts/alembic.sh {command}
    echo 'Done!';
    """
    runner.run_job("aspects", command)


@click.command(help="Dump courses to ClickHouse.")
@click.option("--options", default="")
@click.pass_obj
def dump_courses_to_clickhouse(context, options) -> None:
    """
    Job that proxies the dump_courses_to_clickhouse commands.
    """
    config = tutor_config.load(context.root)
    runner = context.job_runner(config)

    command = f"""
    ./manage.py cms dump_courses_to_clickhouse {options}
    """
    runner.run_job("cms", command)


# pylint: disable=line-too-long
# Ex: tutor local do transform-tracking-logs --options "--source_provider MINIO --source_config '{\"key\": \"openedx\", \"secret\": \"h3SIhXAqDDxJAP6TcXklNxro\", \"container\": \"openedx\", \"prefix\": \"/tracking_logs\", \"host\": \"files.local.overhang.io\", \"secure\": false}' --destination_provider LRS --transformer_type xapi"
@click.command(help="Uses event-routing-backends to replay tracking logs.")
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
@click.pass_obj
def transform_tracking_logs(context, deduplicate, **kwargs) -> None:
    """
    Job that proxies the dump_courses_to_clickhouse commands.
    """
    config = tutor_config.load(context.root)
    runner = context.job_runner(config)

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

    runner.run_job("lms", command)

    if deduplicate:
        runner.run_job(
            "clickhouse",
            env.read_template_file(
                "aspects", "jobs", "init", "clickhouse", "deduplicate.sh"
            ),
        )


COMMANDS = (
    load_xapi_test_data,
    dbt,
    alembic,
    dump_courses_to_clickhouse,
    transform_tracking_logs,
)
