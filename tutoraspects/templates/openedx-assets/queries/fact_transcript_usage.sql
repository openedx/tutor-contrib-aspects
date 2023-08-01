with transcripts as (
    select
        emission_time,
        org,
        course_key,
        video_id,
        actor_id
    from
        {{ DBT_PROFILE_TARGET_DATABASE }}.transcript_usage
    {% raw -%}
    {% if filter_values('org') != [] %}
    where
        org in {{ filter_values('org') | where_in }}
    {% endif %}
    {%- endraw %}
)

select
    transcripts.emission_time as emission_time,
    transcripts.org as org,
    courses.course_name as course_name,
    splitByString('+', courses.course_key)[-1] as run_name,
    blocks.block_name as video_name,
    transcripts.actor_id as actor_id
from
    transcripts
    join {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names courses
         on transcripts.course_key = courses.course_key
    join {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names blocks
         on transcripts.video_id = blocks.location
