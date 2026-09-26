select
    page.org as org,
    page.course_key as course_key,
    page.section_subsection_name as section_subsection_name,
    page.content_level as content_level,
    page.actor_id as actor_id,
    page.section_subsection_page_engagement as section_subsection_page_engagement,
    page.section_with_name as section_with_name,
    page.username as username,
    page.name as name,
    page.email as email
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_pageview_engagement page
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
