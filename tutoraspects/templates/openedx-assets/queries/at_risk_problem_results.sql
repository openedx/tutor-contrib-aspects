select results.*
from {{ DBT_PROFILE_TARGET_DATABASE }}.int_problem_results results
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners using (org, course_key, actor_id)
