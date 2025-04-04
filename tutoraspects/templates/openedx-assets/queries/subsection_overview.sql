with
    last_response as (
        select
            org,
            course_key,
            actor_id,
            object_id,
            problem_id,
            argMax(scaled_score, attempts) as scaled_score,
            MAX(attempts) as last_attempt
        from problem_events
        group by org, course_key, actor_id, object_id, problem_id
    ),
    problem_scores as (
        select
            last_response.org as org,
            last_response.course_key as course_key,
            blocks.subsection_number as subsection_number,
            actor_id,
            toFloat32(last_response.scaled_score) as scaled_score
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks blocks
        join
            last_response
            on blocks.block_id = last_response.problem_id
            and last_response.course_key = blocks.course_key
        where graded
    ),
    section_data as (
        select
            ips.org as org,
            ips.course_key as course_key,
            actor_id,
            ips.subsection_number as subsection_number,
            subsection_blocks.display_name_with_location as subsection_with_name,
            ips.scaled_score
        from problem_scores ips
        left join
            {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks subsection_blocks
            on ips.subsection_number = subsection_blocks.hierarchy_location
            and ips.org = subsection_blocks.org
            and ips.course_key = subsection_blocks.course_key
            and subsection_blocks.block_id like '%@sequential+block@%'
    )
select *
from section_data
