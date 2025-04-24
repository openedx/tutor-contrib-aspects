with
    final_results as (
        select
            last_response.org as org,
            last_response.course_key as course_key,
            last_response.actor_id as actor_id,
            last_response.scaled_score as scaled_score,
            splitByString(
                ' - ', subsection_blocks.display_name_with_location
            ) as _subsection_with_name,
            arrayStringConcat(
                arrayMap(
                    x -> (leftPad(x, 2, char(917768))),
                    splitByString(':', _subsection_with_name[1])
                ),
                ':'
            ) as subsection_number,
            concat(
                subsection_number, ' - ', _subsection_with_name[2]
            ) as subsection_with_name
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_last_response last_response
        join
            {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks problem_blocks
            on problem_blocks.block_id = last_response.problem_id
            and last_response.course_key = problem_blocks.course_key
        left join
            {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks subsection_blocks
            on problem_blocks.subsection_number = subsection_blocks.hierarchy_location
            and last_response.org = subsection_blocks.org
            and last_response.course_key = subsection_blocks.course_key
            and (
                subsection_blocks.block_id like '%@sequential+block@%'
                or subsection_blocks.block_id like '%@chapter+block@%'
            )
        where problem_blocks.graded
    )
select org, course_key, actor_id, subsection_number, subsection_with_name, scaled_score
from final_results
