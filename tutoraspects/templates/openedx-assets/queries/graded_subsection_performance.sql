select
    performance.org as org,
    performance.course_key as course_key,
    performance.block_id as block_id,
    performance.avg_score as avg_score,
    performance.total_avg as total_avg,
    performance.score_range as score_range
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_subsection_performance performance
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
