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
    ),
    {%- endraw %}
    watched_segments as (
        select *
        from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_video_segments
        where 
            org in coalesce({{ filter_values("org") }}, [])
            and course_key in coalesce((select array_concat_agg(course_key) from course_keys), [])
    ),
    watches as (
        select
            segments.org,
            segments.course_key,
            segments.actor_id,
            segments.object_id,
            segments.video_duration,
            segments.watched_segment,
            segments.watch_count,
            segments.watch_count > 1 as rewatched,
            formatDateTime(
                toDate(now()) + toIntervalSecond(segments.watched_segment), '%T'
            ) as time_stamp,
            arrayStringConcat(
                arrayMap(
                    x -> (leftPad(x, 2, char(917768))),
                    splitByString(
                        ':', splitByString(' - ', blocks.display_name_with_location)[1]
                    )
                ),
                ':'
            ) as video_number,
            concat(
                video_number, ' - ', splitByString(' - ', blocks.display_name_with_location)[2]
            ) as video_name_location,
            concat(
                '<a href="',
                segments.object_id,
                '" target="_blank">',
                video_name_location,
                '</a>'
            ) as video_link,
            blocks.section_with_name as section_with_name,
            blocks.subsection_with_name as subsection_with_name
        from watched_segments as segments
        join
            {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks blocks
            on (
                segments.course_key = blocks.course_key
                and splitByString('/xblock/', segments.object_id)[-1] = blocks.block_id
            )
    )
select
    org,
    course_key,
    actor_id,
    object_id,
    splitByChar('@', splitByString('/xblock/', object_id)[-1])[3] as block_id,
    rewatched,
    watched_segment as segment_start,
    sum(watch_count) as watched_count,
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
from watches
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
