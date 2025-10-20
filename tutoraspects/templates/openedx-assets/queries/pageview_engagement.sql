select
    org,
    course_key,
    section_subsection_name,
    content_level,
    actor_id,
    section_subsection_page_engagement,
    section_with_name,
    username,
    name,
    email
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_pageview_engagement
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
