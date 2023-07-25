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
    course_problems.course_name as course_name,
    course_problems.run_name as run_name,
    course_problems.problem_name as problem_name,
    summary.actor_id as actor_id,
    summary.success as success,
    summary.attempts as attempts,
    summary.num_hints_displayed as num_hints_displayed,
    summary.num_answers_displayed as num_answers_displayed
from
    summary
    join course_problems
        on (summary.org = course_problems.org
            and summary.course_key = course_problems.course_key
            and summary.problem_id = course_problems.problem_id)
