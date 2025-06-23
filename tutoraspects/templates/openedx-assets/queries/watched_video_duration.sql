with
    watched_video_segments as (
        {% include 'openedx-assets/queries/watched_video_segments.sql' %}
    ),
    course_data as (
        select
            dim_course_blocks.org as org,
            dim_course_blocks.course_key as course_key,
            count(distinct dim_course_blocks.block_id) video_count,
            dim_course_names.course_name as course_name,
            dim_course_names.course_run as course_run
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks
        left join
            {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_course_names
            on dim_course_blocks.org = dim_course_names.org
            and dim_course_blocks.course_key = dim_course_names.course_key
        where
            dim_course_blocks.block_type = 'video'
            {% include 'openedx-assets/queries/common_filters.sql' %}
        group by org, course_key, course_name, course_run
    )
select
    if(course_data.org = '', watched_video_segments.org, course_data.org) as org,
    if(
        course_data.course_key = '',
        watched_video_segments.course_key,
        course_data.course_key
    ) as course_key,
    course_data.course_name as course_name,
    course_data.course_run as course_run,
    course_data.video_count as video_count,
    watched_video_segments.object_id as object_id,
    watched_video_segments.video_duration as video_duration,
    if(
        video_duration = 0, 0, count(distinct watched_video_segments.segment_start)
    ) as segment_count,
    if(
        video_duration = 0,
        0,
        count(
            distinct case
                when watched_count > 1 then watched_video_segments.segment_start else 0
            end
        )
    ) as segment_count_rewatched,
    watched_video_segments.video_name_location as video_name_location,
    watched_video_segments.block_id as block_id
from course_data
full join
    watched_video_segments on watched_video_segments.course_key = course_data.course_key
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
group by
    org,
    course_key,
    course_name,
    course_run,
    video_count,
    object_id,
    video_duration,
    video_name_location,
    block_id
