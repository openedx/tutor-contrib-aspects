{%- raw -%}
with courses as (
    select
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
        {{ dataset(18) }}
    where
        JSON_VALUE(xblock_data_json, '$.block_type') = 'video'
        {% if filter_values('org') != [] %}
        and org in {{ filter_values('org') | where_in }}
        {% endif %}
), videos as (
    select
        courses.org as org,
        courses.course_name as course_name,
        courses.course_key as course_key,
        courses.run_name as run_name,
        video_blocks.video_id as video_id,
        video_blocks.video_name as video_name
    from
        courses
        join video_blocks
            using (course_key)
), transcripts as (
    select
        emission_time,
        org,
        splitByString('/', course_id)[-1] as course_key,
        video_id,
        actor_id
    from
        reporting.transcript_usage
    {% if filter_values('org') != [] %}
    where
        org in {{ filter_values('org') | where_in }}
    {% endif %}
)

select
    transcripts.emission_time as emission_time,
    transcripts.org as org,
    videos.course_name as course_name,
    videos.run_name as run_name,
    videos.video_name as video_name,
    transcripts.actor_id as actor_id
from
    transcripts
    join videos
        using (org, course_key, video_id)
{%- endraw -%}
