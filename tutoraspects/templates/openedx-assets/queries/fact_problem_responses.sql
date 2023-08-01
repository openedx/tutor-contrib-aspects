with responses as (
    select
        emission_time,
        org,
        course_key,
        problem_id,
        actor_id,
        responses,
        success,
        attempts
    from
        {{ DBT_PROFILE_TARGET_DATABASE }}.problem_responses
    {% raw -%}
    {% if filter_values('org') != [] %}
    where
        org in {{ filter_values('org') | where_in }}
    {% endif %}
    {%- endraw %}
)

select
    responses.emission_time as emission_time,
    responses.org as org,
    courses.course_name as course_name,
    splitByString('+', courses.course_key)[-1] as run_name,
    blocks.block_name as problem_name,
    responses.actor_id as actor_id,
    responses.responses as responses,
    responses.success as success,
    responses.attempts as attempts
from
    responses
    join {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names courses
         on responses.course_key = courses.course_key
    join {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names blocks
         on responses.problem_id = blocks.location
