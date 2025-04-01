with
    last_response as (
        select
            org,
            course_key,
            actor_id,
            object_id,
            problem_id,
            argMax(success, attempts) as success,
            MAX(attempts) as last_attempt
        from problem_events
        group by org, course_key, actor_id, object_id, problem_id
    ),
    problem_results as (
        select
            last_response.org as org,
            last_response.course_key as course_key,
            last_response.actor_id as actor_id,
            blocks.subsection_number as subsection_number,
            last_response.problem_id as problem_id,
            blocks.block_name as problem_name,
            last_response.success,
            blocks.course_order
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks blocks
        join
            last_response
            on blocks.block_id = last_response.problem_id
            and last_response.course_key = blocks.course_key
        where blocks.graded
    )
select
    ips.org as org,
    ips.course_key as course_key,
    splitByString('@', subsection_blocks.block_id)[-1] as block_id,
    ips.subsection_number as subsection_number,
    subsection_blocks.display_name_with_location as subsection_with_name,
    problem_id,
    problem_name,
    actor_id,
    success
from problem_results ips
left join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks subsection_blocks
    on ips.subsection_number = subsection_blocks.hierarchy_location
    and ips.org = subsection_blocks.org
    and ips.course_key = subsection_blocks.course_key
    and subsection_blocks.block_id like '%@sequential+block@%'
