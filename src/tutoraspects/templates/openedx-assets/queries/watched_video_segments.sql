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
    ),
    final_results as (
        select
            watched_segments.org as org,
            watched_segments.course_key as course_key,
            watched_segments.actor_id as actor_id,
            watched_segments.object_id as object_id,
            splitByChar('@', splitByString('/xblock/', watched_segments.object_id)[-1])[
                3
            ] as block_id,
            watched_segments.watched_segment as segment_start,
            sum(watched_segments.watch_count) as watched_count,
            formatDateTime(
                toDate(now()) + toIntervalSecond(watched_segments.watched_segment), '%T'
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
                video_number,
                ' - ',
                splitByString(' - ', blocks.display_name_with_location)[2]
            ) as video_name_location,
            concat(
                '<a href="',
                watched_segments.object_id,
                '" target="_blank">',
                video_name_location,
                '</a>'
            ) as video_link,
            watched_segments.video_duration as video_duration,
            blocks.section_with_name as section_with_name,
            blocks.subsection_with_name as subsection_with_name,
            users.username as username,
            users.name as name,
            users.email as email
        from watched_segments
        left outer join
            {{ DBT_PROFILE_TARGET_DATABASE }}.dim_user_pii users
            on (
                watched_segments.actor_id like 'mailto:%'
                and SUBSTRING(watched_segments.actor_id, 8) = users.email
            )
            or watched_segments.actor_id = toString(users.external_user_id)
        join
            {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks blocks
            on (
                watched_segments.course_key = blocks.course_key
                and splitByString('/xblock/', watched_segments.object_id)[-1]
                = blocks.block_id
            )
        where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
        group by
            org,
            course_key,
            actor_id,
            object_id,
            block_id,
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
    )
select
    org,
    course_key,
    actor_id,
    object_id,
    block_id,
    segment_start,
    watched_count,
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
from final_results
