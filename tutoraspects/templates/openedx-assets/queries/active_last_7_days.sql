with
    recent_activity as (
        select course_key, COUNT(DISTINCT actor_id) as active_last_7_days
        from {{ ASPECTS_XAPI_DATABASE }}.navigation_events
        where
            emission_time >= NOW() - interval 7 DAY
            {% include 'openedx-assets/queries/common_filters.sql' %}
        group by course_key
    )

select fss.*, COALESCE(ra.active_last_7_days, 0) as active_within_last_7_days
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_student_status fss
left join recent_activity ra on fss.course_key = ra.course_key
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
