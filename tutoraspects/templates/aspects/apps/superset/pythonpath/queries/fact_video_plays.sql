{%- raw -%}
with courses as (
    select distinct
        org,
        course_key,
        course_name,
        run_name
    from
        {{ dataset(24) }}
), video_blocks as (
    select
        org,
        course_key,
        location as video_id,
        display_name as video_name
    from
        event_sink.course_blocks
    where
        JSON_VALUE(xblock_data_json, '$.block_type') = 'video'
        {% if filter_values('org') != [] %}
        and org in {{ filter_values('org') | where_in }}
        {% endif %}
), videos as (
    select distinct
        courses.org as org,
        courses.course_key as course_key,
        courses.course_name as course_name,
        courses.run_name as run_name,
        video_blocks.video_id as video_id,
        video_blocks.video_name as video_name
    from
        courses
        join video_blocks
            using (course_key)
), plays as (
    select
        emission_time,
        org,
        splitByString('/course/', course_id)[-1] as course_key,
        actor_id,
        video_id
    from
        reporting.video_plays
)

select
    plays.emission_time as emission_time,
    plays.org as org,
    videos.course_name as course_name,
    videos.run_name as run_name,
    videos.video_name as video_name,
    plays.actor_id as actor_id
from
    plays
    join videos
        using (org, course_key, video_id)
{%- endraw -%}
