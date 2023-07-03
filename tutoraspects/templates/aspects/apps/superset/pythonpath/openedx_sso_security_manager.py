import logging
from collections import namedtuple

import jwt
from authlib.common.urls import add_params_to_qs, add_params_to_uri
from flask import current_app, session
import requests
from superset.security import SupersetSecurityManager
from superset.utils.memoized import memoized

log = logging.getLogger(__name__)


def add_to_headers(token, headers=None):
    """Add a Bearer Token to the request URI.
    Recommended method of passing bearer tokens.
    Authorization: Bearer h480djs93hd8
    """
    headers = headers or {}
    headers["Authorization"] = "JWT {}".format(token)
    return headers


def add_bearer_jwt_token(token, uri, headers, body, placement="header"):
    """Add a Bearer Token to the request."""
    if placement in ("uri", "url", "query"):
        uri = add_params_to_uri(token, uri)
    elif placement in ("header", "headers"):
        headers = add_to_headers(token, headers)
    elif placement == "body":
        body = add_params_to_qs(token, body)
    return uri, headers, body


def create_clickhouse_username(lms_username):
    return f"openedx-{lms_username}"


class OpenEdxSsoSecurityManager(SupersetSecurityManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oauth.oauth2_client_cls.client_cls.token_auth_class.SIGN_METHODS.update(
            {
                "jwt": add_bearer_jwt_token,
            }
        )

    def set_oauth_session(self, provider, oauth_response):
        """
        Store the oauth token in the session for later retrieval.
        """
        res = super().set_oauth_session(provider, oauth_response)

        if provider == "openedxsso":
            session["oauth_token"] = oauth_response
        return res

    def decoded_user_info(self):
        return jwt.decode(
            self.access_token, algorithms=["HS256"], options={"verify_signature": False}
        )

    def oauth_user_info(self, provider, response=None):
        if provider == "openedxsso":
            user_profile = self.decoded_user_info()

            user_roles, user_courses = self._get_user_roles_and_courses(
                user_profile.get("preferred_username")
            )

            clickhouse_username = create_clickhouse_username(
                user_profile["preferred_username"]
            )
            self._create_clickhouse_user(clickhouse_username, user_roles)
            self._insert_user_courses(clickhouse_username, user_courses)

            return {
                "name": user_profile["name"],
                "email": user_profile["email"],
                "id": user_profile["preferred_username"],
                "username": user_profile["preferred_username"],
                "first_name": user_profile.get("given_name")
                or user_profile.get("name", ""),
                "last_name": user_profile.get("family_name"),
                "role_keys": user_roles,
            }

    def get_oauth_token(self, token=None):
        """
        Retrieves the oauth token from the session.

        Returns an empty hash if there is no session.
        """
        # TODO: handle refreshing expired tokens?
        return session.get("oauth_token", {})

    @property
    def access_token(self):
        """
        Returns the string access_token portion of the current OAuth token.
        """
        return self.get_oauth_token().get("access_token")

    def _create_clickhouse_user(self, clickhouse_username, user_roles):
        """
        Create a clickhouse user with appropriate access.
        """
        # FIXME: Should probably make some kind of password hashed off of SECRET_KEY
        #   that we can re-hash for use in the DB_CONNECTION_MUTATOR
        make_clickhouse_query(f"CREATE USER IF NOT EXISTS '{clickhouse_username}' "
                              f"IDENTIFIED BY 'password';")
        make_clickhouse_query(
            f"GRANT CREATE TEMPORARY TABLE ON *.* TO '{clickhouse_username}';"
        )

        self._grant_or_revoke_clickhouse_role(
            clickhouse_username, "openedx_instructor", "openedx" in user_roles
        )
        self._grant_or_revoke_clickhouse_role(
            clickhouse_username, "openedx_superuser", "admin" in user_roles
        )
        self._grant_or_revoke_clickhouse_role(
            clickhouse_username, "openedx_administrator", "alpha" in user_roles
        )

        make_clickhouse_query(f"SET DEFAULT ROLE ALL TO '{clickhouse_username}';")

    def _grant_or_revoke_clickhouse_role(self, clickhouse_username, role_name, grant):
        """
        Grant or revoke a ClickHouse role to a user.
        """
        if grant:
            make_clickhouse_query(f"GRANT {role_name} TO '{clickhouse_username}';")
        else:
            make_clickhouse_query(f"REVOKE {role_name} FROM '{clickhouse_username}';")

    def _insert_user_courses(self, clickhouse_username, courses):
        """
        Inserts rows into ClickHouse for associating users with courses.
        """
        # TODO: Make these parameterized better, this is insecure.
        make_clickhouse_query(f"""
            DELETE FROM 
            {{ ASPECTS_PERMISSIONS_DATABASE }}.{{ ASPECTS_PERMISSIONS_COURSE_MAPPING_TABLE }})
            WHERE clickhouse_username = '{clickhouse_username}';
        """)

        query = f"""INSERT INTO 
            {{ ASPECTS_PERMISSIONS_DATABASE }}.{{ ASPECTS_PERMISSIONS_COURSE_MAPPING_TABLE }}
            (clickhouse_username, course_id) VALUES
        """
        query += "\n".join(f"('{clickhouse_username}', '{c}')," for c in courses)
        make_clickhouse_query(query)

    def _get_user_roles_and_courses(self, username):
        """
        Returns the Superset roles that should be associated with the given user.
        """
        decoded_access_token = self.decoded_user_info()

        if decoded_access_token.get("superuser", False):
            return ["admin", "openedx"], []
        elif decoded_access_token.get("administrator", False):
            return ["alpha", "openedx"], []
        else:
            # User has to have staff access to one or more courses to view any content here.
            courses = self.get_courses(username)
            if courses:
                return ["openedx"], courses
            return [], []

    @memoized(watch=("access_token",))
    def get_courses(self, username, permission="staff", next_url=None):
        """
        Returns the list of courses the current user has access to.
        """
        courses = []
        provider = session.get("oauth_provider")
        oauth_remote = self.oauth_remotes.get(provider)
        if not oauth_remote:
            logging.error("No OAuth2 provider? expected openedx")
            return courses

        token = self.get_oauth_token()
        if not token:
            logging.error("No oauth token? expected one provided by openedx")
            return courses

        openedx_apis = current_app.config["OPENEDX_API_URLS"]
        courses_url = openedx_apis["get_courses"].format(
            username=username, permission=permission
        )
        url = next_url or courses_url
        response = oauth_remote.get(url, token=token).json()

        for course in response.get("results", []):
            course_id = course.get("course_id")
            if course_id:
                courses.append(course_id)

        # Recurse to iterate over all the pages of results
        if response.get("next"):
            next_courses = self.get_courses(
                username, permission=permission, next_url=response["next"]
            )
            for course_id in next_courses:
                courses.append(course_id)

        return courses


def get_clickhouse_admin_url():
   """
   Return the ClickHouse URL with admin creds.
   """
   # FIXME: WE should pull creds from a file or some other way less likely to
   #    break on weird characters.
   auth_scheme = "{% if CLICKHOUSE_SECURE_CONNECTION %}https{% else %}http{% endif %}"
   return f"{auth_scheme}://{{CLICKHOUSE_ADMIN_USER}}:{{CLICKHOUSE_ADMIN_PASSWORD}}@" \
          f"{{CLICKHOUSE_HOST}}:{{CLICKHOUSE_PORT}}/?database={{ASPECTS_XAPI_DATABASE}}"


def make_clickhouse_query(query):
    """
    Query Clickhouse by POSTing some content by http.
    """
    log.warning(query)
    clickhouse_uri = get_clickhouse_admin_url()
    response = requests.post(clickhouse_uri, data=query.encode("utf8"), timeout=10)
    response.raise_for_status()
    return response.content.decode("utf8").strip()


UserAccess = namedtuple("UserAccess", ["username", "is_superuser", "is_staff"])
