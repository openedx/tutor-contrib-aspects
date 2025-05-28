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
    org,
    course_key,
    actor_id,
    object_id,
    splitByChar('@', splitByString('/xblock/', object_id)[-1])[3] as block_id,
    rewatched,
    watched_segment as segment_start,
    count(1) as watched_count,
    time_stamp,
    video_number,
    video_name_location,
    video_link,
    video_duration,
    section_with_name,
    subsection_with_name,
    users.username as username,
    users.name as name,
    users.email as email
from
    {{ DBT_PROFILE_TARGET_DATABASE }}.fact_video_segment_watches(
        {% raw -%}
        org_filter = coalesce({{ filter_values("org") }}, []),
        course_key_filter
        = coalesce((select array_concat_agg(course_key) from course_keys), [])
        {%- endraw %}
    )
left outer join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_user_pii users
    on (actor_id like 'mailto:%' and SUBSTRING(actor_id, 8) = users.email)
    or actor_id = toString(users.external_user_id)
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
group by
    org,
    course_key,
    actor_id,
    object_id,
    block_id,
    rewatched,
    watched_segment,
    time_stamp,
    video_number,
    video_name_location,
    video_link,
    video_duration,
    section_with_name,
    subsection_with_name,
    username,
    name,
    email
