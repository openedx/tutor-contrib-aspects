select
    org,
    course_key,
    course_order,
    problem_link,
    graded,
    actor_id,
    avg_correct_attempts_coursewide,
    avg_incorrect_attempts_coursewide,
    coursewide_percent_correct,
    correct_attempts_by_learner,
    incorrect_attempts_by_learner,
    selected_learner_percent_correct,
    selected_learner_percent_incorrect
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_problem_coursewide_avg
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners using (org, course_key, actor_id)
