with
    first_response as (
        select
            first_response.emission_time as emission_time,
            first_response.org as org,
            first_response.course_key as course_key,
            problem_blocks.block_id as block_id,
            replaceRegexpAll(
                first_response.responses,
                '<.*?hint.*?<\/.*?hint>|</div>|<div>|\[|\]',
                ''
            ) as _response1,
            replaceRegexpAll(_response1, '",(\s|)"', ',') as _response2,
            case
                when first_response.responses like '[%'
                then arrayJoin(splitByChar(',', replaceAll(_response2, '"', '')))
                else _response2
            end as response,
            replaceRegexpAll(
                replaceRegexpAll(first_response.responses, '<div>|</div>|"', ''),
                '\n',
                '<div>'
            ) as responses,
            first_response.success as success,
            first_response.interaction_type as interaction_type,
            substring(
                regexpExtract(
                    first_response.object_id, '(@problem\+block@[\w\d][^_\/]*)(_\d)?', 2
                ),
                2
            ) as _problem_id_number,
            ifNull(nullIf(_problem_id_number, ''), '1') as _problem_id_or_1,
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
        from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_learner_first_response first_response
        left join
            {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks problem_blocks
            on (
                course_key = problem_blocks.course_key
                and problem_id = problem_blocks.block_id
            )
    )
select
    emission_time,
    org,
    course_key,
    toFloat32OrNull(response) as response_numeric,
    case when response_numeric is null then response else '' end as response_string,
    if(success, 'Correct', 'Incorrect') as success,
    interaction_type,
    problem_number,
    problem_name_location,
    splitByChar('@', block_id)[3] as block_id
from first_response
