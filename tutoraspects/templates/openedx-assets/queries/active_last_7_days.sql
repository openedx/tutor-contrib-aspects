with
    recent_activity as (
        select course_key, COUNT(DISTINCT actor_id) as active_last_7_days
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_last_course_visit
        where
            1 = 1
            {% include 'openedx-assets/queries/common_filters.sql' %}
            and emission_time >= subtractDays(now(), 7)
        group by course_key
    )
select
    status.org as org,
    status.course_key as course_key,
    status.actor_id as actor_id,
    status.approving_state as approving_state,
    status.enrollment_mode as enrollment_mode,
    status.enrollment_status as enrollment_status,
    status.course_grade as course_grade,
    status.grade_bucket as grade_bucket,
    status.username as username,
    status.name as name,
    status.email as email,
    status.enrolled_at as enrolled_at,
    status.last_visited as last_visited,
    COALESCE(recent_activity.active_last_7_days, 0) as active_within_last_7_days,
    names.course_name as course_name,
    names.course_run as course_run
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_student_status status
join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names names
    on status.course_key = names.course_key
left join recent_activity on status.course_key = recent_activity.course_key
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
