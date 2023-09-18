from superset.app import create_app

app = create_app()
app.app_context().push()

from superset.connectors.sqla.models import (
    RLSFilterRoles,
    RowLevelSecurityFilter,
    SqlaTable,
)
from superset.extensions import security_manager
from superset.migrations.shared.security_converge import Role

session = security_manager.get_session()

## https://docs.preset.io/docs/row-level-security-rls

VIRTUAL_TABLE_SCHEMA = "main"

SECURITY_FILTERS = [
    {
        "schema": "{{ASPECTS_XAPI_DATABASE}}",
        "table_name": "{{ASPECTS_XAPI_TABLE}}",
        "role_name": "{{SUPERSET_ROLES_MAPPING.instructor}}",
        "group_key": "{{SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY}}",
        "clause": '{% raw %}{{can_view_courses(current_username(), "splitByChar(\'/\', course_id)[-1]")}}{% endraw %}',
        "filter_type": "Regular",
    },
    {
        "schema": VIRTUAL_TABLE_SCHEMA,
        "table_name": "fact_enrollments_by_day",
        "role_name": "{{SUPERSET_ROLES_MAPPING.instructor}}",
        "group_key": "{{SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY}}",
        "clause": '{% raw %}{{can_view_courses(current_username(), "course_key")}}{% endraw %}',
        "filter_type": "Regular"
    },
    {
        "schema": VIRTUAL_TABLE_SCHEMA,
        "table_name": "fact_enrollments",
        "role_name": "{{SUPERSET_ROLES_MAPPING.instructor}}",
        "group_key": "{{SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY}}",
        "clause": '{% raw %}{{can_view_courses(current_username(), "course_key")}}{% endraw %}',
        "filter_type": "Regular"
    },
    {
        "schema": VIRTUAL_TABLE_SCHEMA,
        "table_name": "fact_learner_problem_summary",
        "role_name": "{{SUPERSET_ROLES_MAPPING.instructor}}",
        "group_key": "{{SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY}}",
        "clause": '{% raw %}{{can_view_courses(current_username(), "course_key")}}{% endraw %}',
        "filter_type": "Regular"
    },
    {
        "schema": VIRTUAL_TABLE_SCHEMA,
        "table_name": "fact_problem_responses",
        "role_name": "{{SUPERSET_ROLES_MAPPING.instructor}}",
        "group_key": "{{SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY}}",
        "clause": '{% raw %}{{can_view_courses(current_username(), "course_key")}}{% endraw %}',
        "filter_type": "Regular"
    },
    {
        "schema": VIRTUAL_TABLE_SCHEMA,
        "table_name": "fact_transcript_usage",
        "role_name": "{{SUPERSET_ROLES_MAPPING.instructor}}",
        "group_key": "{{SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY}}",
        "clause": '{% raw %}{{can_view_courses(current_username(), "course_key")}}{% endraw %}',
        "filter_type": "Regular"
    },
    {
        "schema": VIRTUAL_TABLE_SCHEMA,
        "table_name": "fact_video_plays",
        "role_name": "{{SUPERSET_ROLES_MAPPING.instructor}}",
        "group_key": "{{SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY}}",
        "clause": '{% raw %}{{can_view_courses(current_username(), "course_key")}}{% endraw %}',
        "filter_type": "Regular"
    },
    {
        "schema": VIRTUAL_TABLE_SCHEMA,
        "table_name": "fact_watched_video_segments",
        "role_name": "{{SUPERSET_ROLES_MAPPING.instructor}}",
        "group_key": "{{SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY}}",
        "clause": '{% raw %}{{can_view_courses(current_username(), "course_key")}}{% endraw %}',
        "filter_type": "Regular"
    },
    {
        "schema": VIRTUAL_TABLE_SCHEMA,
        "table_name": "hints_per_success",
        "role_name": "{{SUPERSET_ROLES_MAPPING.instructor}}",
        "group_key": "{{SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY}}",
        "clause": '{% raw %}{{can_view_courses(current_username(), "course_key")}}{% endraw %}',
        "filter_type": "Regular"
    },
    {
        "schema": "{{ASPECTS_EVENT_SINK_DATABASE}}",
        "table_name": "course_names",
        "role_name": "{{SUPERSET_ROLES_MAPPING.instructor}}",
        "group_key": "{{SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY}}",
        "clause": '{% raw %}{{can_view_courses(current_username(), "course_key")}}{% endraw %}',
        "filter_type": "Regular"
    },
    {
        "schema": "{{ASPECTS_EVENT_SINK_DATABASE}}",
        "table_name": "course_overviews",
        "role_name": "{{SUPERSET_ROLES_MAPPING.instructor}}",
        "group_key": "{{SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY}}",
        "clause": '{% raw %}{{can_view_courses(current_username(), "course_key")}}{% endraw %}',
        "filter_type": "Regular"
    },
    {
        "schema": "{{ASPECTS_EVENT_SINK_DATABASE}}",
        "table_name": "course_blocks",
        "role_name": "{{SUPERSET_ROLES_MAPPING.instructor}}",
        "group_key": "{{SUPERSET_ROW_LEVEL_SECURITY_XAPI_GROUP_KEY}}",
        "clause": '{% raw %}{{can_view_courses(current_username(), "course_key")}}{% endraw %}',
        "filter_type": "Regular"
    },
]

{{patch("superset-row-level-security") | indent(4)}}


for security_filter in SECURITY_FILTERS:
    # Fetch the table we want to restrict access to
    (
        schema,
        table_name,
        role_name,
        group_key,
        clause,
        filter_type,
    ) = security_filter.values()
    table = (
        session.query(SqlaTable)
        .filter(SqlaTable.schema == schema)
        .filter(SqlaTable.table_name == table_name)
        .first()
    )

    assert table, f"{schema}.{table_name} table doesn't exist yet?"

    role = session.query(Role).filter(Role.name == role_name).first()
    assert role, f"{role_name} role doesn't exist yet?"
    # See if the Row Level Security Filter already exists
    rlsf = (
        session.query(RowLevelSecurityFilter)
        .filter(RLSFilterRoles.c.role_id.in_((role.id,)))
        .filter(RowLevelSecurityFilter.group_key == group_key)
        .filter(RowLevelSecurityFilter.tables.any(id=table.id))
    ).first()
    # If it doesn't already exist, create one
    if rlsf:
        create = False
    else:
        create = True
        rlsf = RowLevelSecurityFilter()
    # Sync the fields to our expectations
    rlsf.filter_type = filter_type
    rlsf.group_key = group_key
    rlsf.tables = [table]
    rlsf.clause = clause
    rlsf.name = f"{table.table_name} - {role.name}"
    # Create if needed
    if create:
        session.add(rlsf)
        # ...and commit, so we are sure to have an rlsf.id
        session.commit()
    # Add the filter role if needed
    rls_filter_roles = (
        session.query(RLSFilterRoles)
        .filter(RLSFilterRoles.c.role_id == role.id)
        .filter(RLSFilterRoles.c.rls_filter_id == rlsf.id)
    )

    if not rls_filter_roles.count():
        session.execute(
            RLSFilterRoles.insert(), [dict(role_id=role.id, rls_filter_id=rlsf.id)]
        )
        session.commit()

print("Successfully create row-level security filters.")
