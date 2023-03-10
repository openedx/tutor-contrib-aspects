#!/usr/bin/env bash
set -e

#
# Always install local overrides first
#
/usr/bin/env bash /app/docker/docker-bootstrap.sh

# Set up a Row-Level Security filter to enforce course-based access restrictions.
# Note: there are no cli commands or REST API endpoints to help us with this,
# so we have to pipe python code directly into the superset shell. Yuck!
superset shell <<EOF
import logging
from superset.connectors.sqla.models import (
    RowLevelSecurityFilter,
    RLSFilterRoles,
    SqlaTable,
)
from superset.utils.core import RowLevelSecurityFilterType
from superset.extensions import security_manager
from superset.migrations.shared.security_converge import Role

session = security_manager.get_session()

# Fetch the Open edX role
role_name = "{{SUPERSET_OPENEDX_ROLE_NAME}}"
openedx_role = session.query(Role).filter(Role.name == role_name).first()
assert openedx_role, "{{SUPERSET_OPENEDX_ROLE_NAME}} role doesn't exist yet?"

# Fetch the xapi table we want to restrict access to
xapi_table = session.query(SqlaTable).filter(
    SqlaTable.schema == "{{OARS_XAPI_DATABASE}}"
).filter(
    SqlaTable.table_name == "{{OARS_XAPI_TABLE}}"
).first()
assert xapi_table, "{{OARS_XAPI_DATABASE}}.{{OARS_XAPI_TABLE}} table doesn't exist yet?"

# See if the Row Level Security Filter already exists
group_key = "{{SUPERSET_XAPI_ROW_LEVEL_SECURITY_COURSE_ID_KEY}}"
xapi_course_id_rls = (
    session.query(
        RowLevelSecurityFilter
    ).filter(
        RLSFilterRoles.c.role_id.in_((openedx_role.id,))
    ).filter(
        RowLevelSecurityFilter.group_key == group_key
    )
).first()

# If it doesn't already exist, create one
if xapi_course_id_rls:
    create = False
else:
    create = True
    xapi_course_id_rls = RowLevelSecurityFilter()

# Sync the fields to our expectations
xapi_course_id_rls.filter_type = RowLevelSecurityFilterType.REGULAR
xapi_course_id_rls.group_key = "xapi_course_id"
xapi_course_id_rls.tables = [xapi_table]
xapi_course_id_rls.clause = (
    {% raw %}
    '{{can_view_courses(current_username(), "splitByChar(\'/\', course_id)[-1]")}}'
    {% endraw %}
)

# Create if needed
if create:
    session.add(xapi_course_id_rls)

# ...and commit, so we are sure to have an xapi_course_id_rls.id
session.commit()

# Add the filter role if needed
rls_filter_roles = (
    session.query(
        RLSFilterRoles
    ).filter(
        RLSFilterRoles.c.role_id == openedx_role.id
    ).filter(
        RLSFilterRoles.c.rls_filter_id == xapi_course_id_rls.id
    )
)

if not rls_filter_roles.count():
    session.execute(RLSFilterRoles.insert(), [
        dict(
            role_id=openedx_role.id,
            rls_filter_id=xapi_course_id_rls.id
        )
    ])
    session.commit()

EOF
# The blank line above EOF is critical -- don't remove it.
