select
    org,
    course_key,
    block_id,
    course_order,
    actor_id,
    page_count,
    section_with_name,
    subsection_with_name,
    visited_on,
    subsection_block_id,
    section_block_id
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_navigation_completion
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
