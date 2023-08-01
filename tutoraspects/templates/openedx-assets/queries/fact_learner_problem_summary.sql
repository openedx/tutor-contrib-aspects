with course_problems as (
    {% include 'openedx-assets/queries/dim_course_problems.sql' %}
), summary as (
    select
        org,
        course_key,
        problem_id,
        actor_id,
        success,
        attempts,
        num_hints_displayed,
        num_answers_displayed
    from {{ DBT_PROFILE_TARGET_DATABASE }}.learner_problem_summary
    {% raw -%}
    {% if filter_values('org') != [] %}
    where
        org in {{ filter_values('org') | where_in }}
    {% endif %}
    {%- endraw %}
)

select
    summary.org as org,
    courses.course_name as course_name,
    splitByString('+', courses.course_key)[-1] as run_name,
    blocks.block_name as problem_name,
    summary.actor_id as actor_id,
    summary.success as success,
    summary.attempts as attempts,
    summary.num_hints_displayed as num_hints_displayed,
    summary.num_answers_displayed as num_answers_displayed
from
    summary
    join {{ ASPECTS_EVENT_SINK_DATABASE }}.course_names courses
         on summary.course_key = courses.course_key
    join {{ ASPECTS_EVENT_SINK_DATABASE }}.course_block_names blocks
         on summary.problem_id = blocks.location
