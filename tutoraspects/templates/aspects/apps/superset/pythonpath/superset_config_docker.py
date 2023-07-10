import os
from urllib.parse import urljoin

from flask_appbuilder.security.manager import AUTH_OAUTH

# Application secret key

SECRET_KEY = os.environ["SECRET_KEY"]

# Don't limit the number of rows that can be used in queries
ROW_LIMIT = int("{{ SUPERSET_ROW_LIMIT }}")
SQL_MAX_ROW = ROW_LIMIT

OPENEDX_LMS_ROOT_URL = os.environ["OPENEDX_LMS_ROOT_URL"]
OPENEDX_API_URLS = {
    "get_courses": urljoin(OPENEDX_LMS_ROOT_URL, os.environ["OPENEDX_COURSES_LIST_PATH"]),
}

# Set the authentication type to OAuth
AUTH_TYPE = AUTH_OAUTH

OAUTH_PROVIDERS = [
    {   'name':'openedxsso',
        'token_key':'access_token', # Name of the token in the response of access_token_url
        'icon':'fa-address-card',   # Icon for the provider
        'remote_app': {
            'client_id': os.environ["OAUTH2_CLIENT_ID"],
            'client_secret': os.environ["OAUTH2_CLIENT_SECRET"],
            'client_kwargs':{
                'scope': 'profile email user_id'               # Scope for the Authorization
            },
            'access_token_method':'POST',    # HTTP Method to call access_token_url
            'access_token_params':{        # Additional parameters for calls to access_token_url
                'client_id': os.environ["OAUTH2_CLIENT_ID"],
                'token_type': 'jwt'
            },
            'access_token_headers':{    # Additional headers for calls to access_token_url
                'Authorization': 'JWT Base64EncodedClientIdAndSecret'
            },
            'api_base_url': OPENEDX_LMS_ROOT_URL,
            'access_token_url': urljoin(OPENEDX_LMS_ROOT_URL, os.environ["OAUTH2_ACCESS_TOKEN_PATH"]),
            'authorize_url': urljoin(OPENEDX_LMS_ROOT_URL, os.environ["OAUTH2_AUTHORIZE_PATH"]),
        }
    }
]

# Will allow user self registration, allowing to create Flask users from Authorized User
AUTH_USER_REGISTRATION = True

# The default user self registration role
AUTH_USER_REGISTRATION_ROLE = "{{SUPERSET_ROLES_MAPPING.instructor}}"

# Should we replace ALL the user's roles each login, or only on registration?
AUTH_ROLES_SYNC_AT_LOGIN = True

# map from the values of `userinfo["role_keys"]` to a list of Superset roles
# cf https://superset.apache.org/docs/security/#roles
AUTH_ROLES_MAPPING = {
    "admin": ["Admin"],      # Superusers
    "alpha": ["Alpha"],      # Global staff
    "gamma": ["Gamma"],      # Course staff
    "instructor": ["{{SUPERSET_ROLES_MAPPING.instructor}}"], # Course instructors
    "operator": ["{{SUPERSET_ROLES_MAPPING.operator}}"], # Installation operators
    "public": ["Public"],    # AKA anonymous users
}

from openedx_sso_security_manager import OpenEdxSsoSecurityManager

CUSTOM_SECURITY_MANAGER = OpenEdxSsoSecurityManager


# Enable use of variables in datasets/queries
FEATURE_FLAGS = {
    "ALERT_REPORTS": True,
    "ENABLE_TEMPLATE_PROCESSING": True,
    "DASHBOARD_RBAC": True,
}

# Add this custom template processor which returns the list of courses the current user can access
from openedx_jinja_filters import *

JINJA_CONTEXT_ADDONS = {
    'can_view_courses': can_view_courses,
    {% for filter in SUPERSET_EXTRA_JINJA_FILTERS %}'{{ filter }}': {{filter}},{% endfor %}
}

{% if not ENABLE_WEB_PROXY %}
# Caddy is running behind a proxy: Superset needs to handle x-forwarded-* headers
# https://flask.palletsprojects.com/en/latest/deploying/proxy_fix/
ENABLE_PROXY_FIX = True
{% endif %}
