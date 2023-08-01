with plays as (
    select
        emission_time,
        org,
        course_key,
        actor_id,
        video_id
    from
        {{ DBT_PROFILE_TARGET_DATABASE }}.video_plays
)

select
    plays.emission_time as emission_time,
    plays.org as org,
    courses.course_name as course_name,
    splitByString('+', courses.course_key)[-1] as run_name,
    blocks.block_name as video_name,
    plays.actor_id as actor_id
from
    plays
    join {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names courses
         on plays.course_key = courses.course_key
    join {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names blocks
         on plays.video_id = blocks.location
