with videos as (
    {% include 'openedx-assets/queries/dim_course_videos.sql' %}
), plays as (
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
    videos.course_name as course_name,
    videos.run_name as run_name,
    videos.video_name as video_name,
    plays.actor_id as actor_id
from
    plays
    join videos
        on (plays.org = videos.org
            and plays.course_key = videos.course_key
            and plays.video_id = videos.video_id)
