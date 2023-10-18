with summary as (
    {% include 'openedx-assets/queries/fact_learner_problem_summary.sql' %}
)

select
    org,
    course_key,
    course_name,
    course_run,
    problem_name,
    problem_name_with_location,
    actor_id,
    sum(num_hints_displayed) + sum(num_answers_displayed) as total_hints
from
    summary
where success = 1
group by
    org,
    course_key,
    course_name,
    course_run,
    problem_name,
    problem_name_with_location,
    actor_id
