"""
Custom Jinja template filters that can be used in Superset queries.

cf https://superset.apache.org/docs/installation/sql-templating/
"""
from superset.extensions import security_manager

ALL_COURSES = "1 = 1"
NO_COURSES = "1 = 0"


def can_view_courses(username, field_name="course_id", **kwargs):
    """
    Returns SQL WHERE clause which restricts access to the courses the current user has
    staff access to.

    We accept kwargs for optional caching args, since this is memoized in
    can_view_courses_wrapper.
    """
    user = security_manager.get_user_by_username(username)
    if user:
        user_roles = security_manager.get_user_roles(user)
    else:
        user_roles = []

    # Users with no roles don't get to see any courses
    if not user_roles:
        return NO_COURSES

    # Superusers and global staff have access to all courses
    for role in user_roles:
        if str(role) == "Admin" or str(role) == "Alpha":
            return ALL_COURSES

    # Everyone else only has access if they're staff on a course.
    courses = security_manager.get_courses(username)

    # TODO: what happens when the list of courses grows beyond what the query will handle?
    if courses:
        course_id_list = ", ".join(f"'{course_id}'" for course_id in courses)
        return f"{field_name} in ({course_id_list})"
    else:
        # If you're not course staff on any courses, you don't get to see any.
        return NO_COURSES


{{patch("superset-jinja-filters")}}
