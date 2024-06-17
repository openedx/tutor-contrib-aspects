with
    enrollments as (
        select
            enrollment.actor_id,
            enrollment.course_key,
            enrollment.org,
            course_names.course_name as course_name
        from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_enrollment_status enrollment
        inner join
            {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names as course_names
            -- Need to cast the course key to a string here otherwise the
            -- course_names dictionary throws this:
            -- Key type for complex key at position 0 does not match, expected String,
            -- found LowCardinality(String).
            on course_names.course_key = enrollment.course_key::String
        where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
    )

select
    users.username as username,
    users.email as email,
    users.name as name,
    enrollments.org as org,
    enrollments.course_key as course_key,
    enrollments.course_name as course_name
from enrollments
inner join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_user_pii as users
    on enrollments.actor_id = users.external_user_id::String
