with
    final_results as (
        select
            last_response.org as org,
            last_response.course_key as course_key,
            last_response.actor_id as actor_id,
            subsection_blocks.block_id as subsection_block_id,
            problem_blocks.block_id as problem_id,
            last_response.success as success,
            substring(
                regexpExtract(
                    last_response.object_id, '(@problem+block@[wd][^_/]*)(_d)?', 2
                ),
                2
            ) as _problem_id_number,
            cast(
                ifNull(nullIf(_problem_id_number, ''), '1') as Int
            ) as _problem_id_or_1,
            splitByString(
                ' - ', problem_blocks.display_name_with_location
            ) as _problem_with_name,
            arrayStringConcat(
                arrayMap(
                    x -> (leftPad(x, 2, char(917768))),
                    splitByString(':', _problem_with_name[1])
                ),
                ':'
            ) as _problem_number,
            concat(_problem_number, '_', _problem_id_or_1) as problem_number,
            concat(
                problem_number, ' - ', _problem_with_name[2]
            ) as problem_name_location
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
select
    org,
    course_key,
    splitByChar('@', subsection_block_id)[3] as block_id,
    problem_number,
    actor_id,
    success
from final_results
