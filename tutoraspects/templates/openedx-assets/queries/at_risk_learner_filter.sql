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

select org, course_key, learners.actor_id as actor_id
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_student_status learners
join page_visits using (org, course_key, actor_id)
where
    approving_state = 'failed' and enrollment_status = 'registered'
    {% include 'openedx-assets/queries/common_filters.sql' %}
