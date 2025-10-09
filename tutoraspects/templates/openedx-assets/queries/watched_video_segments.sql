with
    course_keys as (
        select '' as course_key {% raw -%}
        {% if filter_values("course_name") != [] %}
                {% endraw -%}
            union all
            select course_key as course_key
            from {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names
            where
                course_name in {% raw -%} {{ filter_values("course_name") | where_in }}
        {% endif %}
        {% if filter_values("tag") != [] %}
                {% endraw -%}
            union distinct
            select course_key as course_key
            from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_most_recent_course_tags
            where
                tag in {% raw -%} (
                    select replaceAll(arrayJoin({{ filter_values("tag") }}), '- ', '')
                )
            {% endif %} {% endraw -%}
    ),
    watched_segments as (
        select *
        from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_video_segments
        where
            {% raw -%}
            {% if filter_values("org") != [] %}
                org in {{ filter_values("org") | where_in }} and
            {% endif %} {%- endraw %}
            (
                course_key in (select course_key from course_keys)
                or (select count(1) from course_keys) = 1
            )
    )
select
    watched_segments.org as org,
    watched_segments.course_key as course_key,
    watched_segments.actor_id as actor_id,
    watched_segments.object_id as object_id,
    splitByChar('@', splitByString('/xblock/', watched_segments.object_id)[-1])[3] as block_id,
    watched_segments.watched_segment as segment_start,
    sum(watched_segments.watch_count) as watched_count,
    formatDateTime(
        toDate(now()) + toIntervalSecond(watched_segments.watched_segment), '%T'
    ) as time_stamp,
    watched_segments.video_location as video_location,
    watched_segments.video_name_location as video_name_location,
    watched_segments.video_link as video_link,
    watched_segments.video_duration as video_duration,
    watched_segments.section_with_name as section_with_name,
    watched_segments.subsection_with_name as subsection_with_name,
    users.username as username,
    users.name as name,
    users.email as email
from watched_segments
left outer join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii users
    on (watched_segments.actor_id like 'mailto:%' and SUBSTRING(actor_id, 8) = users.email)
    or watched_segments.actor_id = toString(users.external_user_id)
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
group by
    org,
    course_key,
    actor_id,
    object_id,
    block_id,
    watched_segment,
    time_stamp,
    video_location,
    video_name_location,
    video_link,
    video_duration,
    section_with_name,
    subsection_with_name,
    username,
    name,
    email
