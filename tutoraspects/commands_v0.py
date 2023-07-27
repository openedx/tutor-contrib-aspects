"""Aspects module for tutor v0 commands"""
import click
from tutor import config as tutor_config


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
@click.option("--options", default="")
@click.pass_obj
def transform_tracking_logs(context, options) -> None:
    """
    Job that proxies the dump_courses_to_clickhouse commands.
    """
    config = tutor_config.load(context.root)
    runner = context.job_runner(config)

    command = f"""
    ./manage.py lms transform_tracking_logs {options}
    """
    runner.run_job("lms", command)


COMMANDS = (
    load_xapi_test_data,
    dbt,
    alembic,
    dump_courses_to_clickhouse,
    transform_tracking_logs,
)
