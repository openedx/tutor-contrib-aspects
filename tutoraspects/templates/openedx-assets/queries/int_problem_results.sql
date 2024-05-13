select *
from {{ DBT_PROFILE_TARGET_DATABASE }}.int_problem_results
where 1=1
{% include 'openedx-assets/queries/common_filters.sql' %}
