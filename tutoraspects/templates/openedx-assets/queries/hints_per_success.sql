select
    org,
    course_name,
    run_name,
    problem_name,
    actor_id,
    sum(num_hints_displayed) + sum(num_answers_displayed) as total_hints
from
    {{ DBT_PROFILE_TARGET_DATABASE }}.fact_learner_problem_summary
where success = 1
group by
    org,
    course_name,
    run_name,
    problem_name,
    actor_id
