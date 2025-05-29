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
    repeat_watches as (
        select
            org,
            course_key,
            actor_id,
            object_id,
            splitByString('/xblock/', object_id)[-1] as video_id,
            case
                when rewatched_segment > 0 then 'rewatch' else 'watch'
            end as watch_status,
            case
                when rewatched_segment > 0 then rewatched_segment else watched_segment
            end as segment_start,
            formatDateTime(
                toDate(now()) + toIntervalSecond(segment_start), '%T'
            ) as time_stamp,
            video_duration
        from
            {{ DBT_PROFILE_TARGET_DATABASE }}.fact_video_repeat_watches(
                {% raw -%}
                org_filter = coalesce({{ filter_values("org") }}, []),
                course_key_filter
                = coalesce((select array_concat_agg(course_key) from course_keys), [])
                {%- endraw %}
            )
    ),
    final_results as (
        select
            repeat_watches.org,
            repeat_watches.course_key,
            blocks.course_name,
            blocks.course_run,
            repeat_watches.actor_id,
            repeat_watches.video_id,
            repeat_watches.watch_status,
            repeat_watches.segment_start,
            repeat_watches.time_stamp,
            splitByString(' - ', blocks.display_name_with_location) as _video_with_name,
            arrayStringConcat(
                arrayMap(
                    x -> (leftPad(x, 2, char(917768))),
                    splitByString(':', _video_with_name[1])
                ),
                ':'
            ) as video_number,
            concat(video_number, ' - ', _video_with_name[2]) as video_name_location,
            concat(
                '<a href="',
                repeat_watches.object_id,
                '" target="_blank">',
                blocks.display_name_with_location,
                '</a>'
            ) as video_link,
            repeat_watches.video_duration
        from repeat_watches
        join
            {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks blocks
            on (
                repeat_watches.course_key = blocks.course_key
                and repeat_watches.video_id = blocks.block_id
            )
    )
select
    org,
    course_key,
    actor_id,
    course_name,
    course_run,
    splitByChar('@', video_id)[3] as block_id,
    video_name_location,
    watch_status,
    segment_start,
    time_stamp,
    users.username as username,
    users.name as name,
    users.email as email,
    video_link,
    video_duration
from final_results
left outer join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_user_pii users
    on (actor_id like 'mailto:%' and SUBSTRING(actor_id, 8) = users.email)
    or actor_id = toString(users.external_user_id)
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
