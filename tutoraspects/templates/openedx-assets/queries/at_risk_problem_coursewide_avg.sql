select
    avg.org as org,
    avg.course_key as course_key,
    avg.course_order as course_order,
    avg.problem_link as problem_link,
    avg.graded as graded,
    avg.avg_correct_attempts_coursewide as avg_correct_attempts_coursewide,
    avg.avg_incorrect_attempts_coursewide as avg_incorrect_attempts_coursewide,
    avg.coursewide_percent_correct as coursewide_percent_correct,
    avg.correct_attempts_by_learner as correct_attempts_by_learner,
    avg.incorrect_attempts_by_learner as incorrect_attempts_by_learner,
    avg.selected_learner_percent_correct as selected_learner_percent_correct,
    avg.selected_learner_percent_incorrect as selected_learner_percent_incorrect
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_problem_coursewide_avg avg
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners using (org, course_key, actor_id)
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
