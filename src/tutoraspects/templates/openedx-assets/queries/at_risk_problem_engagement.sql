select distinct
    problem.org as org,
    problem.course_key as course_key,
    problem.section_subsection_name as section_subsection_name,
    problem.section_with_name as section_with_name,
    problem.content_level as content_level,
    problem.actor_id as actor_id,
    problem.section_subsection_problem_engagement
    as section_subsection_problem_engagement,
    problem.block_id as block_id,
    users.username as username,
    users.name as name,
    users.email as email
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_problem_engagement problem
left join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii users
    on (problem.actor_id like 'mailto:%' and SUBSTRING(actor_id, 8) = users.email)
    or problem.actor_id = toString(users.external_user_id)
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners using (org, course_key, actor_id)
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
