#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# This file is included in the final Docker image and SHOULD be overridden when
# deploying the image to prod. Settings configured here are intended for use in local
# development environments. Also note that superset_config_docker.py is imported
# as a final step as a means to override "defaults" configured here
#
"""
Modified from original:

https://github.com/apache/superset/blob/969c963/docker/pythonpath_dev/superset_config.py
"""
import os
from datetime import timedelta
from typing import Optional

from cachelib.redis import RedisCache
from celery.schedules import crontab
from superset.superset_typing import CacheConfig


def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)

SECRET_KEY = os.environ["SECRET_KEY"]

DATABASE_DIALECT = get_env_variable("DATABASE_DIALECT")
DATABASE_USER = get_env_variable("DATABASE_USER")
DATABASE_PASSWORD = get_env_variable("DATABASE_PASSWORD")
DATABASE_HOST = get_env_variable("DATABASE_HOST")
DATABASE_PORT = get_env_variable("DATABASE_PORT")
DATABASE_DB = get_env_variable("DATABASE_DB")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (
    DATABASE_DIALECT,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_DB,
)

REDIS_HOST = get_env_variable("REDIS_HOST")
REDIS_PORT = get_env_variable("REDIS_PORT")
REDIS_CELERY_DB = get_env_variable("REDIS_CELERY_DB", "3")
REDIS_RESULTS_DB = get_env_variable("REDIS_RESULTS_DB", "4")
REDIS_CACHE_DB = get_env_variable("REDIS_CACHE_DB", "5")
REDIS_PASSWORD = get_env_variable("REDIS_PASSWORD", "")

RESULTS_BACKEND = RedisCache(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_RESULTS_DB, key_prefix='superset_results')

CACHE_CONFIG = {
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    'CACHE_REDIS_PASSWORD': REDIS_PASSWORD,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}
DATA_CACHE_CONFIG = CACHE_CONFIG

# Cache for dashboard filter state
FILTER_STATE_CACHE_CONFIG: CacheConfig = {
    "CACHE_DEFAULT_TIMEOUT": 1200,
    # should the timeout be reset when retrieving a cached value
    "REFRESH_TIMEOUT_ON_RETRIEVAL": False,
    **CACHE_CONFIG,
}

# Cache for explore form data state
EXPLORE_FORM_DATA_CACHE_CONFIG: CacheConfig = {
    "CACHE_DEFAULT_TIMEOUT": int(timedelta(days=7).total_seconds()),
    # should the timeout be reset when retrieving a cached value
    "REFRESH_TIMEOUT_ON_RETRIEVAL": True,
    **CACHE_CONFIG,
}

class CeleryConfig(object):
    BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    CELERY_IMPORTS = ("superset.sql_lab", "superset.tasks", "superset.tasks.thumbnails",)
    CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    CELERYD_LOG_LEVEL = "DEBUG"
    CELERYD_PREFETCH_MULTIPLIER = 1
    CELERY_ACKS_LATE = False
    CELERYBEAT_SCHEDULE = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig

# Email configuration
SMTP_HOST = "{{SMTP_HOST}}" # change to your host
SMTP_PORT = {{SMTP_PORT}} # your port, e.g. 587
SMTP_STARTTLS = {{SMTP_USE_TLS}}
SMTP_SSL = {{SMTP_USE_SSL}}
SMTP_USER = "{{SMTP_USERNAME}}" # use the empty string "" if using an unauthenticated SMTP server
SMTP_PASSWORD = "{{SMTP_PASSWORD}}" # use the empty string "" if using an unauthenticated SMTP server
SMTP_MAIL_FROM = "{{CONTACT_EMAIL}}"
EMAIL_REPORTS_SUBJECT_PREFIX = "[{{PLATFORM_NAME}}] "

ALERT_REPORTS_NOTIFICATION_DRY_RUN = False
WEBDRIVER_BASEURL = "http://superset:8088/"
# The base URL for the email report hyperlinks.
WEBDRIVER_BASEURL_USER_FRIENDLY = "{{SUPERSET_HOST}}"

WEBDRIVER_OPTION_ARGS = ["--headless"]

SQLLAB_CTAS_NO_LIMIT = True


{% if SUPERSET_SENTRY_DSN %}
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn='{{ SUPERSET_SENTRY_DSN }}',
    integrations=[FlaskIntegration()],
)
{% endif %}

{% if ENABLE_HTTPS %}
TALISMAN_ENABLED = True
TALISMAN_CONFIG = {
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
}
{% endif %}

{% if LANGUAGE_CODE|lower in SUPERSET_SUPPORTED_LANGUAGES %}
BABEL_DEFAULT_LOCALE = "{{ LANGUAGE_CODE|lower }}"
{% else %}
BABEL_DEFAULT_LOCALE = "en"
print(f"LANGUAGE_CODE='{{ LANGUAGE_CODE|lower }}' not supported by Superset, falling back to 'en'")
{% endif %}

{{ patch('superset-config')}}

# Optionally import superset_config_docker.py (which will have been included on
# the PYTHONPATH) in order to allow for local settings to be overridden
#
try:
    import superset_config_docker
    from superset_config_docker import *  # noqa

    print(f"Loaded your Docker configuration at " f"[{superset_config_docker.__file__}]")
except ImportError:
    print("Using default Docker config...")
