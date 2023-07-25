import logging
from collections import namedtuple

import jwt
from authlib.common.urls import add_params_to_qs, add_params_to_uri
from flask import current_app, session
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

            user_roles = self._get_user_roles(user_profile.get("preferred_username"))

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

    def _get_user_roles(self, username):
        """
        Returns the Superset roles that should be associated with the given user.
        """
        decoded_access_token = self.decoded_user_info()

        if decoded_access_token.get("superuser", False):
            return ["admin", "openedx"]
        elif decoded_access_token.get("administrator", False):
            return ["alpha", "openedx"]
        else:
            # User has to have staff access to one or more courses to view any content here.
            courses = self.get_courses(username)
            if courses:
                return ["openedx"]
            else:
                roles = self.extra_get_user_roles(username, decoded_access_token)
                if bool("{{SUPERSET_BLOCK_STUDENT_ACCESS}}") and not roles:
                    raise Exception(f"Student {username} tried to access Superset")
            return roles if roles else []
    
    def extra_get_user_roles(self, username, decoded_access_token):
        """
        Returns the Superset roles that should be associated with the given user.
        """
        {{ patch("superset-sso-assignment-rules")|indent(8) }}
        return None

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

        # If the user has no staff access to any courses, they are a student
        if not courses and bool("{{SUPERSET_BLOCK_STUDENT_ACCESS}}"):
            raise Exception(f"User {username} is not an instructor")
        else:
            return courses
