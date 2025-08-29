with
    avg_actor as (
        select org, course_key, block_id_short, avg(scaled_score) as avg_score, actor_id
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_subsection_problem_results
        group by org, course_key, block_id_short, actor_id
    ),
    avg_total as (
        select org, course_key, block_id_short, avg(scaled_score) as total_avg
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_subsection_problem_results
        group by org, course_key, block_id_short
    )
select
    avg_actor.org as org,
    avg_actor.course_key as course_key,
    avg_actor.block_id_short as block_id,
    round(avg_actor.avg_score * 100, 2) as avg_score,
    round(avg_total.total_avg, 2) as total_avg,
    case
        when avg_score > 90
        then '>90%'
        when avg_score > 70
        then '71-90%'
        when avg_score > 50
        then '51-70%'
        when avg_score > 30
        then '31-50%'
        when avg_score > 0
        then '1-30%'
        else '0%'
    end as score_range
from avg_actor
join avg_total using (org, course_key, block_id_short)
