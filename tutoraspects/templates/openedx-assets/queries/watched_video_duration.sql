{% raw -%}
with
    course_keys as (
        select [] as course_key
        {% if filter_values("course_name") != [] %}
            union all
            select array(course_key) as course_key
            from
                {% endraw -%} {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names {% raw -%}
            where course_name in {{ filter_values("course_name") | where_in }}
        {% endif %}
        {% if filter_values("tag") != [] %}
            union distinct
            select array(course_key) as course_key
            from
                {% endraw -%} {{ DBT_PROFILE_TARGET_DATABASE }}.dim_most_recent_course_tags {% raw -%}
            where
                tag
                in (select replaceAll(arrayJoin({{ filter_values("tag") }}), '- ', ''))
        {% endif %}
    )
    {%- endraw %}
select
    names.org as org,
    names.course_key as course_key,
    names.course_name as course_name,
    names.course_run as course_run,
    actor_id,
    video_count,
    video_duration,
    watched_time,
    rewatched_time,
    object_id
from
    {{ DBT_PROFILE_TARGET_DATABASE }}.fact_watched_video_duration(
        {% raw -%}
        org_filter = coalesce({{ filter_values("org") }}, []),
        course_key_filter
        = coalesce((select array_concat_agg(course_key) from course_keys), [])
        {%- endraw %}
    ) as a
left join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names as names
    on a.org = names.org
    and a.course_key = names.course_key
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
