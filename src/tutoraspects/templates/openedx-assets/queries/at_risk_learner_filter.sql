with
    page_visits as (
        select org, course_key, actor_id, max(emission_time) as last_visited
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_last_course_visit
        where
            1 = 1
            {% include 'openedx-assets/queries/common_filters.sql' %}
            and emission_time < subtractDays(now(), 7)
        group by org, course_key, actor_id
    )
select
    status.org as org,
    status.course_key as course_key,
    status.actor_id as actor_id,
    page_visits.last_visited as last_visited
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_student_status status
join page_visits using (org, course_key, actor_id)
where
    status.approving_state = 'failed' and status.enrollment_status = 'registered'
    {% include 'openedx-assets/queries/common_filters.sql' %}
