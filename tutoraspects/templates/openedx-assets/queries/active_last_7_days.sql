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
select fss.*, COALESCE(ra.active_last_7_days, 0) as active_within_last_7_days
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_student_status fss
left join recent_activity ra on fss.course_key = ra.course_key
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
