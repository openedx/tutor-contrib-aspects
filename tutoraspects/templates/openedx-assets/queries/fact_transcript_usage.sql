with transcripts as (
select *
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_transcript_usage
where
    1=1
    {% include 'openedx-assets/queries/common_filters.sql' %}
)

select
    emission_time,
    org,
    course_key,
    course_name,
    course_run,
    video_name,
    actor_id
from transcripts
