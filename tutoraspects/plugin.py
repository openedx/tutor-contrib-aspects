"""Implements Aspects plugin via Tutor Plugin API v1."""
from __future__ import annotations

import os.path
import random
import string
from glob import glob

import bcrypt
import pkg_resources
from tutor import hooks

from .__about__ import __version__
from .commands_v0 import COMMANDS as TUTOR_V0_COMMANDS
from .commands_v1 import (
    DO_COMMANDS as TUTOR_V1_DO_COMMANDS,
    COMMANDS as TUTOR_V1_COMMANDS,
)

########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair: (setting_name, default_value).
        # Prefix your setting names with 'ASPECTS_'.
        ("ASPECTS_VERSION", __version__),
        # General tutor specific settings
        ("RUN_VECTOR", True),
        ("RUN_CLICKHOUSE", True),
        ("RUN_RALPH", True),
        ("RUN_SUPERSET", True),
        ("DOCKER_IMAGE_ASPECTS", "edunext/aspects:{{ ASPECTS_VERSION }}"),
        ("DOCKER_IMAGE_CLICKHOUSE", "clickhouse/clickhouse-server:23.8"),
        ("DOCKER_IMAGE_RALPH", "fundocker/ralph:3.9.0"),
        ("DOCKER_IMAGE_SUPERSET", "edunext/aspects-superset:{{ ASPECTS_VERSION }}"),
        ("DOCKER_IMAGE_VECTOR", "timberio/vector:0.30.0-alpine"),
        (
            "OPENEDX_EXTRA_PIP_REQUIREMENTS",
            [
                "openedx-event-sink-clickhouse==0.4.0",
                "edx-event-routing-backends==v7.0.1",
            ],
        ),
        ("EVENT_SINK_CLICKHOUSE_MODELS", ["course_overviews", "user_profile"]),
        ("EVENT_SINK_CLICKHOUSE_PII_MODELS", ["user_profile", "external_id"]),
        # Turning on this flag will store personally identifiable information
        # in the ClickHouse database. Make sure that you understand the legal
        # consequences of data storage and privacy before turning this on!
        ("ASPECTS_ENABLE_PII", False),
        # Markdown comprising the Help tab for the Operator and Instructor dashboards.
        # Set to empty string/False to omit Help tab entirely from the dashboard.
        # Newlines and double-quotes must be escaped.
        (
            "ASPECTS_INSTRUCTOR_HELP_MARKDOWN",
            "## Help\\n"
            "* [Aspects Reference](https://docs.openedx.org/projects/openedx-aspects/page/"
            "reference/instructor_reports.html)\\n"
            "* [Superset Resources](https://github.com/apache/superset#resources)\\n",
        ),
        (
            "ASPECTS_OPERATOR_HELP_MARKDOWN",
            "## Help\\n"
            "* [Aspects Reference](https://docs.openedx.org/projects/openedx-aspects/page/"
            "reference/operator_reports.html)\\n"
            "* [Superset Resources](https://github.com/apache/superset#resources)\\n",
        ),
        # ClickHouse xAPI settings
        ("ASPECTS_XAPI_DATABASE", "xapi"),
        ("ASPECTS_RAW_XAPI_TABLE", "xapi_events_all"),
        ("ASPECTS_XAPI_TRANSFORM_MV", "xapi_events_all_parsed_mv"),
        ("ASPECTS_XAPI_TABLE", "xapi_events_all_parsed"),
        # ClickHouse top-level materialized views
        ("ASPECTS_ENROLLMENT_TRANSFORM_MV", "enrollment_events_mv"),
        ("ASPECTS_ENROLLMENT_EVENTS_TABLE", "enrollment_events"),
        ("ASPECTS_VIDEO_PLAYBACK_TRANSFORM_MV", "video_playback_events_mv"),
        ("ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE", "video_playback_events"),
        ("ASPECTS_PROBLEM_TRANSFORM_MV", "problem_events_mv"),
        ("ASPECTS_PROBLEM_EVENTS_TABLE", "problem_events"),
        ("ASPECTS_NAVIGATION_TRANSFORM_MV", "navigation_events_mv"),
        ("ASPECTS_NAVIGATION_EVENTS_TABLE", "navigation_events"),
        ("ASPECTS_GRADING_TRANSFORM_MV", "grading_events_mv"),
        ("ASPECTS_GRADING_EVENTS_TABLE", "grading_events"),
        ("ASPECTS_FORUM_TRANSFORM_MV", "forum_events_mv"),
        ("ASPECTS_FORUM_EVENTS_TABLE", "forum_events"),
        ("ASPECTS_COMPLETION_EVENTS_TABLE", "completion_events"),
        ("ASPECTS_COMPLETION_TRANSFORM_MV", "completion_events_mv"),
        # ClickHouse event sink settings
        ("ASPECTS_EVENT_SINK_DATABASE", "event_sink"),
        ("ASPECTS_EVENT_SINK_NODES_TABLE", "course_blocks"),
        ("ASPECTS_EVENT_SINK_RELATIONSHIPS_TABLE", "course_relationships"),
        ("ASPECTS_EVENT_SINK_OVERVIEWS_TABLE", "course_overviews"),
        ("ASPECTS_EVENT_SINK_USER_PROFILE_TABLE", "user_profile"),
        ("ASPECTS_EVENT_SINK_CLICKHOUSE_TIMEOUT_SECS", "5"),
        ("ASPECTS_EVENT_SINK_RECENT_BLOCKS_TABLE", "most_recent_course_blocks"),
        ("ASPECTS_EVENT_SINK_RECENT_BLOCKS_MV", "most_recent_course_blocks_mv"),
        # Vector settings
        ("ASPECTS_DOCKER_HOST_SOCK_PATH", "/var/run/docker.sock"),
        ("ASPECTS_VECTOR_DATABASE", "openedx"),
        ("ASPECTS_VECTOR_RAW_TRACKING_LOGS_TABLE", "_tracking"),
        ("ASPECTS_VECTOR_RAW_XAPI_TABLE", "xapi_events_all"),
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
        # This can be used to override some configuration values in
        # via "docker_config.xml" file, which will be read from a
        # mount on /etc/clickhouse-server/config.d/ on startup.
        # See https://clickhouse.com/docs/en/operations/configuration-files
        #
        # This default allows connecting to Clickhouse when run as a
        # standalone docker container, instead of through docker-compose.
        (
            "CLICKHOUSE_EXTRA_XML_CONFIG",
            """
    <!-- Port for HTTP API. See also 'https_port' for secure connections.
         This interface is also used by ODBC and JDBC drivers (DataGrip, Dbeaver, ...)
         and by most of web interfaces (embedded UI, Grafana, Redash, ...).
    -->
    <http_port>{{CLICKHOUSE_INTERNAL_HTTP_PORT}}</http_port>

    <!-- Port for interaction by native protocol with:
         - clickhouse-client and other native ClickHouse tools (clickhouse-benchmark,
           clickhouse-copier);
         - clickhouse-server with other clickhouse-servers for distributed query processing;
         - ClickHouse drivers and applications supporting native protocol
         (this protocol is also informally called as "the TCP protocol");
         See also 'tcp_port_secure' for secure connections.
    -->
    <tcp_port>{{CLICKHOUSE_INTERNAL_NATIVE_PORT}}</tcp_port>

    <listen_host>::</listen_host>
    <listen_host>0.0.0.0</listen_host>
    <listen_try>1</listen_try>
        """,
        ),
        # Override configuration in users.xml. Similar to CLICKHOUSE_EXTRA_XML_CONFIG,
        # this will be read from a mount on /etc/clickhouse-server/users.d/
        # on startup
        # The http settings revert back to the value from versions pre-23.6,
        # when the default was changed from 1Mb to 128Kb
        (
            "CLICKHOUSE_EXTRA_USERS_XML_CONFIG",
            """
    <profiles>
        <default>
            <http_max_field_value_size>1048576</http_max_field_value_size>
            <http_max_field_name_size>1048576</http_max_field_name_size>
        </default>
    </profiles>
            """,
        ),
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
            "@{{CLICKHOUSE_HOST}}:{{CLICKHOUSE_INTERNAL_NATIVE_PORT}}/{{"
            "ASPECTS_XAPI_DATABASE}}"
            "{% if CLICKHOUSE_SECURE_CONNECTION %}?secure=True{% endif %}",
        ),
        ######################
        # Ralph Settings
        # Change to https:// if the public interface to it is secure
        ("RALPH_HOST", "ralph"),
        ("RALPH_PORT", "8100"),
        ("RALPH_ENABLE_PUBLIC_URL", False),
        ("RALPH_RUN_HTTPS", False),
        ("RALPH_SENTRY_DSN", ""),
        ("RALPH_EXECUTION_ENVIRONMENT", "development"),
        ("RALPH_SENTRY_CLI_TRACES_SAMPLE_RATE", 1.0),
        ("RALPH_SENTRY_LRS_TRACES_SAMPLE_RATE", 0.1),
        ("RALPH_SENTRY_IGNORE_HEALTH_CHECKS", True),
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
        (
            "SUPERSET_EMBEDDABLE_DASHBOARDS",
            {
                "instructor-dashboard": "1d6bf904-f53f-47fd-b1c9-6cd7e284d286",
            },
        ),
        ("SUPERSET_ADMIN_EMAIL", "admin@openedx.org"),
        ("SUPERSET_LMS_EMAIL", "superset/lms-admin@aspects.invalid"),
        ("SUPERSET_OWNERS", []),
        # Set to 0 to have no row limit.
        ("SUPERSET_ROW_LIMIT", 100_000),
        (
            "SUPERSET_METADATA_SQLALCHEMY_URI",
            "mysql://{{SUPERSET_DB_USERNAME}}:{{SUPERSET_DB_PASSWORD}}"
            "@{{SUPERSET_DB_HOST}}/{{SUPERSET_DB_METADATA_NAME}}",
        ),
        ("SUPERSET_SENTRY_DSN", ""),
        (
            "SUPERSET_TALISMAN_CONFIG",
            {
                "content_security_policy": {
                    "default-src": ["'self'", "'unsafe-inline'", "'unsafe-eval'"],
                    "img-src": ["'self'", "data:"],
                    "worker-src": ["'self'", "blob:"],
                    "connect-src": [
                        "'self'",
                        "https://api.mapbox.com",
                        "https://events.mapbox.com",
                    ],
                    "object-src": "'none'",
                }
            },
        ),
        ("SUPERSET_TALISMAN_ENABLED", True),
        # These are languages that Superset itself supports, it does not currently
        # support different locales for a language.
        ("SUPERSET_DEFAULT_LOCALE", "en"),
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
        # This controls the cache time of the user's course list
        # only, limiting the number of LMS calls since they are
        # rate limited. This can be cleared by logging back in.
        ("SUPERSET_USER_COURSES_CACHE_TIMEOUT", 300),
        ("SUPERSET_BLOCK_STUDENT_ACCESS", True),
        # This setting allows Superset to run behind a reverse proxy in HTTPS and
        # redirect to the correct http/s based on the headers sent from the proxy.
        # By default it is on if Caddy is enabled, but it can be set separately in
        # case you are running a different proxy or otherwise have different needs.
        ("SUPERSET_ENABLE_PROXY_FIX", "{{ENABLE_WEB_PROXY}}"),
        ######################
        # dbt Settings
        # For the most part you shouldn't have to touch these
        # DBT_PROFILE_* settings get passed into the dbt_profile.yml file.
        # For now we are pulling this from github, which should allow maximum
        # flexibility for forking, running branches, specific versions, etc.
        ("DBT_REPOSITORY", "https://github.com/openedx/aspects-dbt"),
        ("DBT_BRANCH", "v2.7"),
        # Path to the dbt project inside the repository
        ("DBT_REPOSITORY_PATH", "aspects-dbt"),
        # This is a pip compliant list of Python packages to install to run dbt
        # make sure packages with versions are enclosed in double quotes
        ("EXTRA_DBT_PACKAGES", []),
        # This is the name of the database dbt will write to
        ("DBT_PROFILE_TARGET_DATABASE", "reporting"),
        # Validate TLS certificate if using TLS/SSL
        ("DBT_PROFILE_VERIFY", "True"),
        # Use TLS (native protocol) or HTTPS (http protocol)
        ("DBT_PROFILE_SECURE", "{{ CLICKHOUSE_SECURE_CONNECTION }}"),
        # Number of times to retry a "retryable" database exception (such as a 503
        # 'Service Unavailable' error)
        ("DBT_PROFILE_RETRIES", "3"),
        # Use gzip compression if truthy (http), or compression type for a native
        # connection
        ("DBT_PROFILE_COMPRESSION", "lz4"),
        # Timeout in seconds to establish a connection to ClickHouse
        ("DBT_PROFILE_CONNECT_TIMEOUT", "10"),
        # Timeout in seconds to receive data from the ClickHouse server
        ("DBT_PROFILE_SEND_RECEIVE_TIMEOUT", "300"),
        # Use specific settings designed to improve operation on replicated databases
        # (recommended for ClickHouse Cloud)
        ("DBT_PROFILE_CLUSTER_MODE", "False"),
        # Use the experimental `delete+insert` as the default incremental strategy.
        ("DBT_PROFILE_USE_LW_DELETES", "False"),
        # Validate that clickhouse support the atomic EXCHANGE TABLES command.  (Not
        # needed for most ClickHouse versions)
        ("DBT_PROFILE_CHECK_EXCHANGE", "False"),
        # A dictionary/mapping of custom ClickHouse settings for the connection -
        # default is empty.
        ("DBT_PROFILE_CUSTOM_SETTINGS", ""),
        # Allows the connection to understand the JSON type
        ("DBT_PROFILE_ALLOW_EXPERIMENTAL_OBJECT_TYPE", "True"),
        # Timeout for server ping
        ("DBT_PROFILE_SYNC_REQUEST_TIMEOUT", "5"),
        # Compression block size if compression is enabled, this is the default value
        ("DBT_PROFILE_COMPRESS_BLOCK_SIZE", "1048576"),
    ]
)

# Ralph requires us to write out a file with pre-encrypted values, so we encrypt
# them here per: https://openfun.github.io/ralph/api/#creating_a_credentials_file
#
# They will remain unchanged between config saves as usual and the unencryted
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
    ("lms", ("aspects", "jobs", "init", "init-lms.sh"), 97),
]

# For each task added to MY_INIT_TASKS, we load the task template
# and add it to the CLI_DO_INIT_TASKS filter, which tells Tutor to
# run it as part of the `init` job.
try:
    for service, template_path, priority in MY_INIT_TASKS:
        hooks.Filters.COMMANDS_INIT.add_item(
            (service, template_path)
        )  # pylint: disable=no-member
except AttributeError as e:
    for service, template_path, priority in MY_INIT_TASKS:
        full_path: str = pkg_resources.resource_filename(
            "tutoraspects", os.path.join("templates", *template_path)
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
        pkg_resources.resource_filename("tutoraspects", "templates"),
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
        pkg_resources.resource_filename("tutoraspects", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))

########################################
# CUSTOM JOBS (a.k.a. "do-commands")
########################################
# To keep compatibility with tutor14 we need to add the commands
# directly to the dev|k8s|local command groups.
try:
    CLI_DO_COMMANDS = hooks.Filters.CLI_DO_COMMANDS
except AttributeError:
    from tutor.commands import dev, k8s, local

    for f in TUTOR_V0_COMMANDS:
        for mode in [dev.dev, local.local, k8s.k8s]:
            mode.add_command(f)
else:
    for f in TUTOR_V1_DO_COMMANDS:
        CLI_DO_COMMANDS.add_item(f)

# These commands work in both versions, but we're keeping them in the V1
# file for now.
for f in TUTOR_V1_COMMANDS:
    hooks.Filters.CLI_COMMANDS.add_item(f)
