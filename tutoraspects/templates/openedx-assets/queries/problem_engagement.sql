select
    problem.org as org,
    problem.course_key as course_key,
    problem.section_subsection_name as section_subsection_name,
    problem.section_with_name as section_with_name,
    problem.content_level as content_level,
    problem.actor_id as actor_id,
    problem.section_subsection_problem_engagement
    as section_subsection_problem_engagement,
    problem.block_id as block_id,
    problem.username as username,
    problem.name as name,
    problem.email as email
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_problem_engagement problem
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
