select org, course_key, block_id, total_avg, score_range, score_range_count
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_subsection_performance
