select
    results.org as org,
    results.course_key as course_key,
    results.block_id_short as block_id,
    results.actor_id as actor_id,
    case
        when round(avg(results.scaled_score) * 100, 2) > 90
        then '>90%'
        when round(avg(results.scaled_score) * 100, 2) > 70
        then '71-90%'
        when round(avg(results.scaled_score) * 100, 2) > 50
        then '51-70%'
        when round(avg(results.scaled_score) * 100, 2) > 30
        then '31-50%'
        when round(avg(results.scaled_score) * 100, 2) > 0
        then '1-30%'
        else '0%'
    end as score_range,
    avg(results.scaled_score) as avg_score
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_subsection_problem_results results
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
group by results.org, results.course_key, results.block_id_short, results.actor_id
