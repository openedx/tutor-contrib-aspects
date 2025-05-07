"""Implements Aspects plugin via Tutor Plugin API v1."""

from __future__ import annotations

import os.path
import random
import string
import typing as t
from glob import glob

import bcrypt
import importlib_resources
from tutor import hooks
from tutormfe.hooks import PLUGIN_SLOTS

from .__about__ import __version__
from .commands_v1 import COMMANDS as TUTOR_V1_COMMANDS
from .commands_v1 import DO_COMMANDS as TUTOR_V1_DO_COMMANDS

########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair: (setting_name, default_value).
        # Prefix your setting names with 'ASPECTS_'.
        ("ASPECTS_VERSION", __version__),
        # For out default deployment we currently use Celery -> Ralph for transport,
        # so Vector is off by default.
        ("RUN_VECTOR", False),
        ("RUN_CLICKHOUSE", True),
        ("RUN_RALPH", True),
        ("RUN_SUPERSET", True),
        ("DOCKER_IMAGE_ASPECTS", "edunext/aspects:{{ ASPECTS_VERSION }}"),
        ("DOCKER_IMAGE_CLICKHOUSE", "clickhouse/clickhouse-server:25.3"),
        ("DOCKER_IMAGE_RALPH", "fundocker/ralph:4.1.0"),
        ("DOCKER_IMAGE_SUPERSET", "edunext/aspects-superset:{{ ASPECTS_VERSION }}"),
        ("DOCKER_IMAGE_VECTOR", "timberio/vector:0.30.0-alpine"),
        (
            "EVENT_SINK_MODELS_ENABLED",
            ["course_overviews", "tag", "taxonomy", "object_tag", "course_enrollment"],
        ),
        (
            "EVENT_SINK_PII_MODELS",
            ["user_profile", "external_id", "auth_user"],
        ),
        # Turning on this flag will store personally identifiable information
        # in the ClickHouse database. Make sure that you understand the legal
        # consequences of data storage and privacy before turning this on!
        ("ASPECTS_ENABLE_PII", False),
        ("ASPECTS_ENABLE_EVENT_BUS_CONSUMER", False),
        ("ASPECTS_ENABLE_EVENT_BUS_PRODUCER", False),
        ("ASPECTS_EVENT_BUS_CONSUMER_REPLICAS", 1),
        # These settings override the event-routing-backends defaults for performance
        # reasons.
        # Turn on event batching by default, performance is severely impacted by
        # turning this off.
        ("EVENT_ROUTING_BACKEND_BATCHING_ENABLED", True),
        # Events are sent when they hit either the batch size or the batch interval
        # time limit (defaults here are 100 events or 5 seconds).
        # https://event-routing-backends.readthedocs.io/en/latest/getting_started.html#batching-configuration
        ("EVENT_ROUTING_BACKEND_BATCH_SIZE", 100),
        ("EVENT_ROUTING_BACKEND_BATCH_INTERVAL", 5),
        # User PII is cached in an in-memory dictionary for this many seconds.
        ("ASPECTS_PII_CACHE_LIFETIME", 900),
        # Markdown comprising the Help tab for the Operator and Instructor dashboards.
        # Set to empty string/False to omit Help tab entirely from the dashboard.
        # Newlines and double-quotes must be escaped.
        (
            "ASPECTS_COURSE_OVERVIEW_HELP_MARKDOWN",
            "## Help<br>"
            "* [Aspects Reference](https://docs.openedx.org/projects/openedx-aspects/page/"
            "reference/course_overview_dashboard.html)<br>"
            "* [Superset Resources](https://github.com/apache/superset#resources)<br>",
        ),
        (
            "ASPECTS_LEARNER_GROUPS_HELP_MARKDOWN",
            "## Help<br>"
            "* [Aspects Reference](https://docs.openedx.org/projects/openedx-aspects/page/"
            "reference/learner_groups_dashboard.html)<br>"
            "* [Superset Resources](https://github.com/apache/superset#resources)<br>",
        ),
        (
            "ASPECTS_OPERATOR_HELP_MARKDOWN",
            "## Help<br>"
            "* [Aspects Reference](https://docs.openedx.org/projects/openedx-aspects/page/"
            "reference/operator_reports.html)<br>"
            "* [Superset Resources](https://github.com/apache/superset#resources)<br>",
        ),
        (
            "ASPECTS_INDIVIDUAL_LEARNER_HELP_MARKDOWN",
            "## Help<br>"
            "* [Aspects Reference](https://docs.openedx.org/projects/openedx-aspects/page/"
            "reference/individual_learner_dashboard.html)<br>"
            "* [Superset Resources](https://github.com/apache/superset#resources)<br>",
        ),
        (
            "ASPECTS_COURSE_COMPARISON_HELP_MARKDOWN",
            "## Help<br>"
            "* [Aspects Reference](https://docs.openedx.org/projects/openedx-aspects/page/"
            "reference/course_comparison_dashboard.html)<br>"
            "* [Superset Resources](https://github.com/apache/superset#resources)<br>",
        ),
        ("ASPECTS_ENABLE_INSTRUCTOR_DASHBOARD_PLUGIN", True),
        # Whether to show the link to go to Superset in the instructor dashboard tab
        ("SUPERSET_SHOW_INSTRUCTOR_DASHBOARD_LINK", True),
        # The following settings are used to configure the Superset dashboards
        # in the LMS Instructor Dashboard.
        (
            "ASPECTS_INSTRUCTOR_DASHBOARDS",
            [
                {
                    "name": "Course Dashboard",
                    "slug": "course-dashboard",
                    "uuid": "c0e64194-33d1-4d5a-8c10-4f51530c5ee9",
                    "allow_translations": True,
                },
                {
                    "name": "At-Risk Learners Dashboard",
                    "slug": "learner-groups",
                    "uuid": "8661d20c-cee6-4245-9fcc-610daea5fd24",
                    "allow_translations": True,
                },
                {
                    "name": "Individual Learner Dashboard",
                    "slug": "individual-learner",
                    "uuid": "abae8a25-1ba4-4653-81bd-d3937a162a11",
                    "allow_translations": True,
                },
            ],
        ),
        # The following settings are used to configure the Superset dashboards
        # that can be embedded. Keeping separate settings as these may not be
        # directly used in the LMS Instructor Dashboard.
        (
            "SUPERSET_EMBEDDABLE_DASHBOARDS",
            {
                "course-dashboard": "c0e64194-33d1-4d5a-8c10-4f51530c5ee9",
                "learner-groups": "8661d20c-cee6-4245-9fcc-610daea5fd24",
                "individual-learner": "abae8a25-1ba4-4653-81bd-d3937a162a11",
                "in-context-course": "f2880cc1-63e9-48d7-ac3c-d2ff6f6698e2",
                "in-context-graded-subsection": "f0321087-6428-4b97-b32e-2dae7d9cc447",
                "in-context-problem": "98ff33ff-18dd-48f9-8c58-629ae4f4194b",
                "in-context-video": "bc6510fb-027f-4026-a333-d0c42d3cc35c",
            },
        ),
        (
            "SUPERSET_DASHBOARDS",
            {
                "course-comparison": "c6c7062d-dd90-4292-b9cf-84f7b9f38e73",
                # Leaving this out for now while query context is generated
                # for operator-dashboard slices.
                # "operator-dashboard": "02c0121c-40e9-4d8a-b86a-6b996a1cc6fe",
            },
        ),
        # ClickHouse xAPI settings
        ("ASPECTS_XAPI_DATABASE", "xapi"),
        ("ASPECTS_RAW_XAPI_TABLE", "xapi_events_all"),
        # ClickHouse event sink settings
        ("ASPECTS_EVENT_SINK_DATABASE", "event_sink"),
        ("ASPECTS_EVENT_SINK_CLICKHOUSE_TIMEOUT_SECS", 5),
        # Vector settings
        ("ASPECTS_DOCKER_HOST_SOCK_PATH", "/var/run/docker.sock"),
        ("ASPECTS_VECTOR_STORE_TRACKING_LOGS", False),
        ("ASPECTS_VECTOR_STORE_XAPI", True),
        ("ASPECTS_VECTOR_DATABASE", "openedx"),
        ("ASPECTS_VECTOR_RAW_TRACKING_LOGS_TABLE", "_tracking"),
        ("ASPECTS_VECTOR_RAW_XAPI_TABLE", "xapi_events_all"),
        ("ASPECTS_DATA_TTL_EXPRESSION", "toDateTime(emission_time) + INTERVAL 1 YEAR"),
        # Make sure LMS / CMS have event-routing-backends installed
        ######################
        # ClickHouse Settings
        # Note! ClickHouse has several reserved ports, make sure you are not reusing
        # a taken port: https://clickhouse.com/docs/en/guides/sre/network-ports
        ("CLICKHOUSE_HOST", "clickhouse"),
        # If you are using ClickHouse in a clustered environment, place the name of
        # the cluster here. All objects will be created "ON CLUSTER" with replicated
        # table types, otherwise a single server deployment will be assumed.
        ("CLICKHOUSE_CLUSTER_NAME", ""),
        # We need to connect to a single node for Alembic and dbt DDL queries,
        # otherwise the fast pace of the changes will outpace the propagation of
        # changes to the cluster. We assume connection details are all the same
        # except for the host.
        ("CLICKHOUSE_CLUSTER_DDL_NODE_HOST", ""),
        # Port for the native interface exposed on the host container in Docker Compose,
        # this is changed from 9000 to prevent conflicts with MinIO, which also listens
        # on 9000.
        ("CLICKHOUSE_HOST_INSECURE_NATIVE_PORT", "9006"),
        # Port for the native interface ClickHouse will open on the container, used in
        # internal networking on the cluster.
        ("CLICKHOUSE_INTERNAL_INSECURE_NATIVE_PORT", "9000"),
        # Port for the TLS native encrypted native interface exposed on the host
        # container in Docker Compose.
        ("CLICKHOUSE_HOST_TLS_NATIVE_PORT", "9440"),
        # Port for the TLS native interface ClickHouse will open on the container
        ("CLICKHOUSE_INTERNAL_TLS_NATIVE_PORT", "9440"),
        # Use the secure ports if we're configured for them, otherwise insecure
        (
            "CLICKHOUSE_HOST_NATIVE_PORT",
            "{% if CLICKHOUSE_SECURE_CONNECTION %}"
            "{{CLICKHOUSE_HOST_TLS_NATIVE_PORT}}"
            "{% else %}"
            "{{CLICKHOUSE_HOST_INSECURE_NATIVE_PORT}}"
            "{% endif %}",
        ),
        (
            "CLICKHOUSE_INTERNAL_NATIVE_PORT",
            "{% if CLICKHOUSE_SECURE_CONNECTION %}"
            "{{CLICKHOUSE_INTERNAL_TLS_NATIVE_PORT}}"
            "{% else %}"
            "{{CLICKHOUSE_INTERNAL_INSECURE_NATIVE_PORT}}"
            "{% endif %}",
        ),
        # Port for the HTTP interface exposed on the host container in Docker Compose.
        ("CLICKHOUSE_HOST_INSECURE_HTTP_PORT", "8123"),
        # Port for the HTTP interface ClickHouse will open on the container, used in
        # internal networking on the cluster.
        ("CLICKHOUSE_INTERNAL_INSECURE_HTTP_PORT", "8123"),
        # Port for the TLS HTTP encrypted HTTP interface exposed on the host
        # container in Docker Compose.
        ("CLICKHOUSE_HOST_TLS_HTTP_PORT", "8443"),
        # Port for the TLS HTTP interface ClickHouse will open on the container
        ("CLICKHOUSE_INTERNAL_TLS_HTTP_PORT", "8443"),
        # Use the secure ports if we're configured for them, otherwise insecure
        (
            "CLICKHOUSE_HOST_HTTP_PORT",
            "{% if CLICKHOUSE_SECURE_CONNECTION %}"
            "{{CLICKHOUSE_HOST_TLS_HTTP_PORT}}"
            "{% else %}"
            "{{CLICKHOUSE_HOST_INSECURE_HTTP_PORT}}"
            "{% endif %}",
        ),
        (
            "CLICKHOUSE_INTERNAL_HTTP_PORT",
            "{% if CLICKHOUSE_SECURE_CONNECTION %}"
            "{{CLICKHOUSE_INTERNAL_TLS_HTTP_PORT}}"
            "{% else %}"
            "{{CLICKHOUSE_INTERNAL_INSECURE_HTTP_PORT}}"
            "{% endif %}",
        ),
        ("CLICKHOUSE_K8S_VOLUME_SIZE", "10Gi"),
        (
            "CLICKHOUSE_URL",
            "{{CLICKHOUSE_HOST}}:{{CLICKHOUSE_INTERNAL_HTTP_PORT}}",
        ),
        (
            "CLICKHOUSE_REPORT_URL",
            "{{ASPECTS_CLICKHOUSE_REPORT_USER}}:{{ASPECTS_CLICKHOUSE_REPORT_PASSWORD}}"
            "@{{CLICKHOUSE_URL}}/{{ASPECTS_XAPI_DATABASE}}",
        ),
        (
            "CLICKHOUSE_REPORT_SQLALCHEMY_URI",
            "clickhousedb+connect://{{CLICKHOUSE_REPORT_URL}}",
        ),
        (
            "CLICKHOUSE_ADMIN_SQLALCHEMY_URI",
            "clickhouse+native://{{CLICKHOUSE_ADMIN_USER}}:{{CLICKHOUSE_ADMIN_PASSWORD}}"
            "@"
            "{% if CLICKHOUSE_CLUSTER_DDL_NODE_HOST %}"
            "{{CLICKHOUSE_CLUSTER_DDL_NODE_HOST}}"
            "{% else %}"
            "{{CLICKHOUSE_HOST}}"
            "{% endif %}"
            ":{{CLICKHOUSE_INTERNAL_NATIVE_PORT}}/{{ASPECTS_XAPI_DATABASE}}"
            "{% if CLICKHOUSE_SECURE_CONNECTION %}?secure=True{% endif %}",
        ),
        ######################
        # Ralph Settings
        # Change to https:// if the public interface to it is secure
        ("RALPH_HOST", "ralph"),
        ("RALPH_PORT", "8100"),
        ("RALPH_ENABLE_PUBLIC_URL", False),
        ("RALPH_RUN_HTTPS", False),
        ("RALPH_EXTRA_SETTINGS", {}),
        ######################
        # Superset Settings
        ("SUPERSET_HOST", "superset.{{ LMS_HOST }}"),
        ("SUPERSET_PORT", "8088"),
        ("SUPERSET_DB_DIALECT", "mysql"),
        ("SUPERSET_DB_HOST", "{{ MYSQL_HOST }}"),
        ("SUPERSET_DB_PORT", "{{ MYSQL_PORT }}"),
        ("SUPERSET_DB_NAME", "superset"),
        ("SUPERSET_DB_USERNAME", "superset"),
        ("SUPERSET_DB_METADATA_NAME", "superset"),
        ("SUPERSET_EXTRA_REQUIREMENTS", []),
        ("SUPERSET_OAUTH2_ACCESS_TOKEN_PATH", "/oauth2/access_token/"),
        ("SUPERSET_OAUTH2_AUTHORIZE_PATH", "/oauth2/authorize/"),
        (
            "SUPERSET_OPENEDX_COURSES_LIST_PATH",
            "/api/courses/v1/courses/?permissions={permission}&username={username}",
        ),
        ("SUPERSET_OPENEDX_PREFERENCE_PATH", "api/user/v1/preferences/{username}"),
        (
            "SUPERSET_ROLES_MAPPING",
            {
                "instructor": "Instructor",
                "operator": "Operator",
                "admin": "Admin",
                "student": "Student",
            },
        ),
        ("SUPERSET_ADMIN_EMAIL", "admin@openedx.org"),
        ("SUPERSET_LMS_EMAIL", "superset/lms-admin@aspects.invalid"),
        ("SUPERSET_OWNERS", []),
        # Set to 0 to have no row limit.
        (
            "SUPERSET_METADATA_SQLALCHEMY_URI",
            "mysql://{{SUPERSET_DB_USERNAME}}:{{SUPERSET_DB_PASSWORD}}"
            "@{{SUPERSET_DB_HOST}}/{{SUPERSET_DB_METADATA_NAME}}",
        ),
        (
            "SUPERSET_DATABASES",
            {
                "OpenedX Clickhouse": "{{CLICKHOUSE_REPORT_SQLALCHEMY_URI}}",
                "Superset Metadata": "{{SUPERSET_METADATA_SQLALCHEMY_URI}}",
            },
        ),
        # These are languages that Superset itself supports, it does not currently
        # support different locales for a language.
        (
            "SUPERSET_SUPPORTED_LANGUAGES",
            {
                "en": {"flag": "us", "name": "English"},
                "es": {"flag": "es", "name": "Español"},
                "it": {"flag": "it", "name": "Italian"},
                "fr": {"flag": "fr", "name": "French"},
                "zh": {"flag": "cn", "name": "Chinese"},
                "ja": {"flag": "jp", "name": "Japanese"},
                "de": {"flag": "de", "name": "German"},
                "pt": {"flag": "pt", "name": "Portuguese"},
                "ru": {"flag": "ru", "name": "Russian"},
                "ko": {"flag": "kr", "name": "Korean"},
                "sk": {"flag": "sk", "name": "Slovak"},
                "sl": {"flag": "si", "name": "Slovenian"},
                "nl": {"flag": "nl", "name": "Dutch"},
            },
        ),
        # These are the locales that Open edX supports according to:
        # https://openedx.atlassian.net/wiki/spaces/COMM/pages/3157524644/Translation+Working+Group
        (
            "SUPERSET_DASHBOARD_LOCALES",
            [
                "ar",
                "da",
                "de_DE",
                "el",
                "en",
                "es_419",
                "es_ES",
                "fr_CA",
                "he",
                "hi",
                "id",
                "it_IT",
                "pt_BR",
                "pt_PT",
                "ru",
                "th",
                "tr_TR",
                "uk",
                "zh_CN",
            ],
        ),
        ("SUPERSET_EXTRA_JINJA_FILTERS", {}),
        # This controls the cache time of the can_view_courses
        # wrapper, which controls the course-based permissions.
        # This includes the user roles and course list. This
        # does not get cleared on login, and so should be kept
        # short since mostly most of the savings comes from the
        # course cache anyway.
        ("SUPERSET_USER_PERMISSIONS_CACHE_TIMEOUT", 120),
        ("SUPERSET_BLOCK_STUDENT_ACCESS", True),
        ("SUPERSET_BLOCK_INSTRUCTOR_ACCESS", False),
        # This setting allows Superset to run behind a reverse proxy in HTTPS and
        # redirect to the correct http/s based on the headers sent from the proxy.
        # By default it is on if Caddy is enabled, but it can be set separately in
        # case you are running a different proxy or otherwise have different needs.
        ("SUPERSET_ENABLE_PROXY_FIX", "{{ENABLE_WEB_PROXY}}"),
        # This setting allows operators to automatically refresh the datasets
        # in the Superset database. This is useful for keeping the columns up to
        # date with the latest changes in DBT.
        ("SUPERSET_REFRESH_DATASETS", False),
        ("SUPERSET_SENTRY_DSN", ""),
        ######################
        # dbt Settings
        # For the most part you shouldn't have to touch these
        # DBT_PROFILE_* settings get passed into the dbt_profile.yml file.
        # For now we are pulling this from github, which should allow maximum
        # flexibility for forking, running branches, specific versions, etc.
        ("DBT_REPOSITORY", "https://github.com/openedx/aspects-dbt"),
        ("DBT_BRANCH", "v4.0.2"),
        ("DBT_SSH_KEY", ""),
        ("DBT_STATE_DIR", "/app/aspects-dbt/state"),
        ("DBT_PROFILES_DIR", "/app/aspects/dbt/"),
        # This is the name of the database dbt will write to
        ("DBT_PROFILE_TARGET_DATABASE", "reporting"),
        ("RUN_ASPECTS_DOCS", False),
        ("DBT_HOST", "dbt.{{LMS_HOST}}"),
        #####################
        # MFE Customizations
        # Aspects can enable plugins to show in-context metrics in the Authoring MFE.
        # This requires the authroring MFE to have sidebar slots and header
        # slots which is availabe in release Teak and above. This is also
        # dependent on https://github.com/openedx/frontend-plugin-aspects.
        # The feature also needs the platform-plugin-aspect to have v1.1.0 and
        # above.
        ("ASPECTS_ENABLE_STUDIO_IN_CONTEXT_METRICS", False),
    ]
)

# Ralph requires us to write out a file with pre-encrypted values, so we encrypt
# them here per: https://openfun.github.io/ralph/api/#creating_a_credentials_file
#
# They will remain unchanged between config saves as usual and the unencrypted
# passwords will still be able to be printed.
RALPH_ADMIN_PASSWORD = "".join(random.choice(string.ascii_lowercase) for i in range(36))
RALPH_LMS_PASSWORD = "".join(random.choice(string.ascii_lowercase) for i in range(36))
RALPH_ADMIN_HASHED_PASSWORD = bcrypt.hashpw(
    RALPH_ADMIN_PASSWORD.encode(), bcrypt.gensalt()
).decode("ascii")
RALPH_LMS_HASHED_PASSWORD = bcrypt.hashpw(
    RALPH_LMS_PASSWORD.encode(), bcrypt.gensalt()
).decode("ascii")

hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # LRS user is used by Ralph to write to the ClickHouse xAPI tables
        ("ASPECTS_CLICKHOUSE_LRS_USER", "ch_lrs"),
        ("ASPECTS_CLICKHOUSE_LRS_PASSWORD", "{{ 24|random_string }}"),
        # Vector user is used by Vector to write to the ClickHouse tracking log
        # and xAPI tables
        ("ASPECTS_CLICKHOUSE_VECTOR_USER", "ch_vector"),
        ("ASPECTS_CLICKHOUSE_VECTOR_PASSWORD", "{{ 24|random_string }}"),
        # Report user is used by Superset to read from ClickHouse tables
        ("ASPECTS_CLICKHOUSE_REPORT_USER", "ch_report"),
        ("ASPECTS_CLICKHOUSE_REPORT_PASSWORD", "{{ 24|random_string }}"),
        # CMS user is used by CMS to insert into event sink tables
        ("ASPECTS_CLICKHOUSE_CMS_USER", "ch_cms"),
        ("ASPECTS_CLICKHOUSE_CMS_PASSWORD", "{{ 24|random_string }}"),
        ######################
        # ClickHouse Settings
        ("CLICKHOUSE_ADMIN_USER", "ch_admin"),
        ("CLICKHOUSE_ADMIN_PASSWORD", "{{ 24|random_string }}"),
        ("CLICKHOUSE_SECURE_CONNECTION", False),
        ######################
        # Ralph Settings
        ("RALPH_ADMIN_USERNAME", "ralph"),
        ("RALPH_ADMIN_PASSWORD", RALPH_ADMIN_PASSWORD),
        ("RALPH_ADMIN_HASHED_PASSWORD", RALPH_ADMIN_HASHED_PASSWORD),
        ("RALPH_LMS_USERNAME", "lms"),
        ("RALPH_LMS_PASSWORD", RALPH_LMS_PASSWORD),
        ("RALPH_LMS_HASHED_PASSWORD", RALPH_LMS_HASHED_PASSWORD),
        ######################
        # Superset Settings
        ("SUPERSET_SECRET_KEY", "{{ 24|random_string }}"),
        ("SUPERSET_DB_PASSWORD", "{{ 24|random_string }}"),
        ("SUPERSET_OAUTH2_CLIENT_ID", "{{ 16|random_string }}"),
        ("SUPERSET_OAUTH2_CLIENT_ID_DEV", "{{ 16|random_string }}"),
        ("SUPERSET_OAUTH2_CLIENT_SECRET", "{{ 16|random_string }}"),
        ("SUPERSET_ADMIN_USERNAME", "{{ 12|random_string }}"),
        ("SUPERSET_ADMIN_PASSWORD", "{{ 24|random_string }}"),
        ("SUPERSET_LMS_USERNAME", "{{ 12|random_string }}"),
        ("SUPERSET_LMS_PASSWORD", "{{ 24|random_string }}"),
    ]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    [
        # Danger zone!
        # Add values to override settings from Tutor core or other plugins here.
        # Each override is a pair: (setting_name, new_value). For example:
        ### ("PLATFORM_NAME", "My platform"),
        # Superset overrides
        ("SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY", "xapi_course_id"),
    ]
)


def _aspects_public_hosts(
    hosts: list[str], context_name: t.Literal["local", "dev"]
) -> list[str]:
    if context_name == "dev":
        hosts += ["{{ SUPERSET_HOST }}:{{ SUPERSET_PORT }}"]
    else:
        hosts += ["{{ SUPERSET_HOST }}"]
    return hosts


try:
    hooks.Filters.APP_PUBLIC_HOSTS.add(_aspects_public_hosts)
except AttributeError:
    pass


@hooks.Filters.IMAGES_BUILD_MOUNTS.add()
def _mount_superset_on_build(
    mounts: list[tuple[str, str]], host_path: str
) -> list[tuple[str, str]]:
    """
    Automatically add superset repo from the host to the build context whenever
    it is added to the `MOUNTS` setting.
    """
    if os.path.basename(host_path) == "superset":
        mounts += [
            ("aspects-superset", "superset"),
        ]
    return mounts


@hooks.Filters.COMPOSE_MOUNTS.add()
def _mount_superset_compose(
    volumes: list[tuple[str, str]], name: str
) -> list[tuple[str, str]]:
    """
    When mounting superset with `tutor mounts add /path/to/superset"
    bind-mount the host repo in the superset container.
    """
    if name == "superset":
        volumes += [("superset", "/app")]
    return volumes


########################################
# INITIALIZATION TASKS
########################################

# To add a custom initialization task, create a bash script template under:
# tutoraspects/templates/aspects/jobs/init/
# and then add it to the MY_INIT_TASKS list. Each task is in the format:
# ("<service>", ("<path>", "<to>", "<script>", "<template>"))
MY_INIT_TASKS: list[tuple[str, tuple[str, ...], int]] = [
    ("mysql", ("aspects", "jobs", "init", "mysql", "init-mysql.sh"), 92),
    ("clickhouse", ("aspects", "jobs", "init", "clickhouse", "init-clickhouse.sh"), 93),
    ("aspects", ("aspects", "jobs", "init", "aspects", "init-aspects.sh"), 94),
    ("superset", ("aspects", "jobs", "init", "superset", "init-superset.sh"), 95),
    ("mysql", ("aspects", "jobs", "init", "mysql", "init-mysql-post-migration.sh"), 96),
    ("lms", ("aspects", "jobs", "init", "lms", "init-lms.sh"), 97),
]

# For each task added to MY_INIT_TASKS, we load the task template
# and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# run it as part of the `init` job.
try:
    for service, template_path, priority in MY_INIT_TASKS:
        hooks.Filters.COMMANDS_INIT.add_item(
            (service, template_path)
        )  # pylint: disable=no-member
except AttributeError:
    for service, template_path, priority in MY_INIT_TASKS:
        full_path = os.path.join(
            str(importlib_resources.files("tutoraspects") / "templates"), *template_path
        )
        with open(full_path, encoding="utf-8") as init_task_file:
            init_task: str = init_task_file.read()
        hooks.Filters.CLI_DO_INIT_TASKS.add_item(
            (service, init_task), priority=priority
        )

########################################
# DOCKER IMAGE MANAGEMENT
########################################


# Images to be built by `tutor images build`.
# Each item is a quadruple in the form:
#     ("<tutor_image_name>", ("path", "to", "build", "dir"), "<docker_image_tag>", "<build_args>")
hooks.Filters.IMAGES_BUILD.add_items(
    [
        (
            "aspects-superset",
            ("plugins", "aspects", "build", "aspects-superset"),
            "{{DOCKER_IMAGE_SUPERSET}}",
            (),
        ),
        (
            "aspects",
            ("plugins", "aspects", "build", "aspects"),
            "{{DOCKER_IMAGE_ASPECTS}}",
            (),
        ),
    ]
)

# Images to be pulled as part of `tutor images pull`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PULL.add_items(
    [
        (
            "aspects-superset",
            "{{DOCKER_IMAGE_SUPERSET}}",
        ),
        (
            "aspects",
            "{{DOCKER_IMAGE_ASPECTS}}",
        ),
    ]
)

# Images to be pushed as part of `tutor images push`.
# Each item is a pair in the form:
#     ("<tutor_image_name>", "<docker_image_tag>")
hooks.Filters.IMAGES_PUSH.add_items(
    [
        (
            "aspects-superset",
            "{{DOCKER_IMAGE_SUPERSET}}",
        ),
        (
            "aspects",
            "{{DOCKER_IMAGE_ASPECTS}}",
        ),
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
        str(importlib_resources.files("tutoraspects") / "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``source_path/destination_path`` (relative to your Tutor environment).
    # For example, ``tutoraspects/templates/aspects/build``
    # will be rendered to ``$(tutor config printroot)/env/plugins/aspects/build``.
    [
        ("aspects/build", "plugins"),
        ("aspects/apps", "plugins"),
    ],
)

########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutoraspects/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        str(importlib_resources.files("tutoraspects") / "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))

########################################
# CUSTOM JOBS (a.k.a. "do-commands")
########################################
CLI_DO_COMMANDS = hooks.Filters.CLI_DO_COMMANDS

for f in TUTOR_V1_DO_COMMANDS:
    CLI_DO_COMMANDS.add_item(f)

# These commands work in both versions, but we're keeping them in the V1
# file for now.
for f in TUTOR_V1_COMMANDS:
    hooks.Filters.CLI_COMMANDS.add_item(f)

# Autoscaling
try:
    from tutoraspects.filters import (  # pylint: disable=unused-import
        add_aspects_autoscaling,
    )
except ImportError:
    pass


########################################
# MFE Customizations
########################################

PLUGIN_SLOTS.add_items(
    [
        (
            "authoring",
            "course_authoring_outline_sidebar_slot",
            """
          {
            op: PLUGIN_OPERATIONS.Insert,
            widget: {
                id: 'outline-sidebar',
                priority: 1,
                type: DIRECT_PLUGIN,
                RenderWidget: CourseOutlineSidebar,
            },
          }""",
        ),
        (
            "authoring",
            "course_authoring_outline_sidebar_slot",
            """
          {
            op: PLUGIN_OPERATIONS.Wrap,
            widgetId: 'default_contents',
            wrapper: SidebarToggleWrapper,
          }""",
        ),
        (
            "authoring",
            "course_authoring_unit_sidebar_slot",
            """
          {
            op: PLUGIN_OPERATIONS.Insert,
            widget: {
                id: 'course-unit-sidebar',
                priority: 1,
                type: DIRECT_PLUGIN,
                RenderWidget: UnitPageSidebar,
            },
          }""",
        ),
        (
            "authoring",
            "course_authoring_unit_sidebar_slot",
            """
          {
            op: PLUGIN_OPERATIONS.Wrap,
            widgetId: 'default_contents',
            wrapper: SidebarToggleWrapper,
          }""",
        ),
        (
            "authoring",
            "course_unit_header_actions_slot",
            """
          {
              op: PLUGIN_OPERATIONS.Insert,
              widget: {
                  id: 'unit-header-aspects-button',
                  priority: 60,
                  type: DIRECT_PLUGIN,
                  RenderWidget: CourseHeaderButton,
              },
          }""",
        ),
        (
            "authoring",
            "course_outline_header_actions_slot",
            """
          {
              op: PLUGIN_OPERATIONS.Insert,
              widget: {
                  id: 'outline-header-aspects-button',
                  priority: 60,
                  type: DIRECT_PLUGIN,
                  RenderWidget: CourseHeaderButton,
              },
          }""",
        ),
        (
            "authoring",
            "course_outline_unit_card_extra_actions_slot",
            """
          {
            op: PLUGIN_OPERATIONS.Insert,
            widget: {
                id: 'units-action-aspects-button',
                priority: 60,
                type: DIRECT_PLUGIN,
                RenderWidget: UnitActionsButton,
            },
          }""",
        ),
        (
            "authoring",
            "course_outline_subsection_card_extra_actions_slot",
            """
          {
            op: PLUGIN_OPERATIONS.Insert,
            widget: {
                id: 'units-action-aspects-button',
                priority: 60,
                type: DIRECT_PLUGIN,
                RenderWidget: SubSectionAnalyticsButton,
            },
          }""",
        ),
    ]
)
