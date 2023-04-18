from __future__ import annotations

import os
import os.path
from glob import glob

import click
import pkg_resources
from tutor import hooks

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair: (setting_name, default_value).
        # Prefix your setting names with 'OARS_'.
        ("OARS_VERSION", __version__),

        # ClickHouse xAPI settings
        ("OARS_XAPI_DATABASE", "xapi"),
        ("OARS_RAW_XAPI_TABLE", "xapi_events_all"),
        ("OARS_XAPI_TRANSFORM_MV", "xapi_events_all_parsed_mv"),
        ("OARS_XAPI_TABLE", "xapi_events_all_parsed"),

        # ClickHouse Coursegraph setting
        ("OARS_COURSEGRAPH_DATABASE", "coursegraph"),
        ("OARS_COURSEGRAPH_NODES_TABLE", "coursegraph_nodes"),
        ("OARS_COURSEGRAPH_RELATIONSHIPS_TABLE", "coursegraph_relationships"),

        # MySQL dataset settings
        ("OARS_SUPERSET_ENROLLMENTS_TABLE", "Course Enrollments Overview"),

        # Make sure LMS / CMS have evnet-routing-backends installed
        # TODO: Do a new release and pin this! Also add config!
        ("OPENEDX_EXTRA_PIP_REQUIREMENTS", ["edx-event-routing-backends"]),
    ]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # Add settings that don't have a reasonable default for all users here.
        # For instance: passwords, secret keys, etc.
        # Each new setting is a pair: (setting_name, unique_generated_value).
        # Prefix your setting names with 'OARS_'.
        # For example:
        ### ("OARS_SECRET_KEY", "{{ 24|random_string }}"),

        # Note! The CLICKHOUSE_ADMIN_USER is managed in the ClickHouse plugin.

        # LRS user is used by Ralph to insert into ClickHouse aXPI tables
        ("OARS_CLICKHOUSE_LRS_USER", "ch_lrs"),
        ("OARS_CLICKHOUSE_LRS_PASSWORD", "{{ 24|random_string }}"),

        # Report user is used by Superset to read from ClickHouse tables
        ("OARS_CLICKHOUSE_REPORT_USER", "ch_report"),
        ("OARS_CLICKHOUSE_REPORT_PASSWORD", "{{ 24|random_string }}"),

        # CMS user is used by CMS to insert into Coursegraph tables
        ("OARS_CLICKHOUSE_CMS_USER", "ch_cms"),
        ("OARS_CLICKHOUSE_CMS_PASSWORD", "{{ 24|random_string }}"),
    ]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    [
        # Danger zone!
        # Add values to override settings from Tutor core or other plugins here.
        # Each override is a pair: (setting_name, new_value). For example:
        ### ("PLATFORM_NAME", "My platform"),
        # Superset overrides
        ("SUPERSET_XAPI_DASHBOARD_SLUG", "openedx-xapi"),
        ("SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY", "xapi_course_id"),
        ("SUPERSET_ROW_LEVEL_SECURITY_ENROLLMENTS_GROUP_KEY", "enrollments_course_id"),
    ]
)


########################################
# INITIALIZATION TASKS
########################################

# To add a custom initialization task, create a bash script template under:
# tutoroars/templates/oars/jobs/init/
# and then add it to the MY_INIT_TASKS list. Each task is in the format:
# ("<service>", ("<path>", "<to>", "<script>", "<template>"))
MY_INIT_TASKS: list[tuple[str, tuple[str, ...], int]] = [
    ("oars", ("oars", "jobs", "init", "oars_init_schemas_tables_users.sh"), 96),
    ("oars", ("oars", "jobs", "init", "superset-api-dashboard.sh"), 98),
    ("superset", ("oars", "jobs", "init", "superset-init-security.sh"), 99),
    ("lms", ("oars", "jobs", "init", "configure-oars-lms.sh"), 100),
]


# For each task added to MY_INIT_TASKS, we load the task template
# and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# run it as part of the `init` job.
for service, template_path, priority in MY_INIT_TASKS:
    full_path: str = pkg_resources.resource_filename(
        "tutoroars", os.path.join("templates", *template_path)
    )
    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
    hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task), priority=priority)


########################################
# DOCKER IMAGE MANAGEMENT
########################################


# Images to be built by `tutor images build`.
# Each item is a quadruple in the form:
#     ("<tutor_image_name>", ("path", "to", "build", "dir"), "<docker_image_tag>", "<build_args>")
hooks.Filters.IMAGES_BUILD.add_items(
    [
        # To build `myimage` with `tutor images build myimage`,
        # you would add a Dockerfile to templates/oars/build/myimage,
        # and then write:
        ### (
        ###     "myimage",
        ###     ("plugins", "oars", "build", "myimage"),
        ###     "docker.io/myimage:{{ OARS_VERSION }}",
        ###     (),
        ### ),
    ]
)


# Images to be pulled as part of `tutor images pull`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PULL.add_items(
    [
        # To pull `myimage` with `tutor images pull myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ OARS_VERSION }}",
        ### ),
    ]
)


# Images to be pushed as part of `tutor images push`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PUSH.add_items(
    [
        # To push `myimage` with `tutor images push myimage`, you would write:
        ### (
        ###     "myimage",
        ###     "docker.io/myimage:{{ OARS_VERSION }}",
        ### ),
    ]
)


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        pkg_resources.resource_filename("tutoroars", "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutoroars/templates/oars/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/oars/build``.
    [
        ("oars/build", "plugins"),
        ("oars/apps", "plugins"),
    ],
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutoroars/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutoroars", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))


########################################
# CUSTOM JOBS (a.k.a. "do-commands")
########################################
# Ex: "tutor dev do load-xapi-test-data"
@click.command()
@click.option("-n", "--num_batches", default=100)
@click.option("-s", "--batch_size", default=100)
def load_xapi_test_data(num_batches: int, batch_size: int) -> list[tuple[str, str]]:
    """
    Job that loads bogus test xAPI data to ClickHouse via Ralph.
    """
    return [
        ("oars", "echo 'Making demo xapi script executable...' && "
                 "chmod +x /app/oars/scripts/clickhouse-demo-xapi-data.sh && "
                 "echo 'Done. Running script...' && "
                 f"bash /app/oars/scripts/clickhouse-demo-xapi-data.sh {num_batches} {batch_size} && "
                 "echo 'Done!';"),
    ]


# Add the command function to CLI_DO_COMMANDS:
hooks.Filters.CLI_DO_COMMANDS.add_item(load_xapi_test_data)


#######################################
# CUSTOM CLI COMMANDS
#######################################

# Your plugin can also add custom commands directly to the Tutor CLI.
# These commands are run directly on the user's host computer
# (unlike jobs, which are run in containers).

# To define a command group for your plugin, you would define a Click
# group and then add it to CLI_COMMANDS:


### @click.group()
### def oars() -> None:
###     pass


### hooks.Filters.CLI_COMMANDS.add_item(oars)


# Then, you would add subcommands directly to the Click group, for example:


### @oars.command()
### def example_command() -> None:
###     """
###     This is helptext for an example command.
###     """
###     print("You've run an example command.")


# This would allow you to run:
#   $ tutor oars example-command
