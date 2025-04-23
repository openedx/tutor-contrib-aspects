with
    problem_events as (
        select
            emission_time as emission_time,
            org as org,
            course_key as course_key,
            block_id as block_id,
            replaceRegexpAll(
                responses, '<.*?hint.*?<\/.*?hint>|</div>|<div>|\[|\]', ''
            ) as _response1,
            replaceRegexpAll(_response1, '",(\s|)"', ',') as _response2,
            case
                when responses like '[%'
                then arrayJoin(splitByChar(',', replaceAll(_response2, '"', '')))
                else _response2
            end as response,
            replaceRegexpAll(
                replaceRegexpAll(responses, '<div>|</div>|"', ''), '\n', '<div>'
            ) as responses,
            success as success,
            interaction_type as interaction_type,
            substring(
                regexpExtract(object_id, '(@problem\+block@[\w\d][^_\/]*)(_\d)?', 2), 2
            ) as _problem_id_number,
            ifNull(nullIf(_problem_id_number, ''), '1') as _problem_id_or_1,
            splitByString(' - ', blocks.display_name_with_location)[
                1
            ] as _problem_location,
            splitByString('-', blocks.display_name_with_location)[2] as _problem_name,
            if(
                blocks.display_name_with_location = '',
                '',
                concat(_problem_location, '(', _problem_id_or_1, ')', _problem_name)
            ) as problem_name_with_location,
            blocks.display_name_with_location as display_name_with_location
        from {{ ASPECTS_XAPI_DATABASE }}.problem_events
        left join
            {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks blocks
            on (course_key = blocks.course_key and problem_id = blocks.block_id)
        where attempts = 1
    )
select
    emission_time,
    org,
    course_key,
    splitByString('@', block_id)[-1] as block_id,
    toFloat32OrNull(response) as response_numeric,
    if(success, 'Correct', 'Incorrect') as success,
    interaction_type,
    problem_name_with_location,
    case when response_numeric is null then response else '' end as response_string,
    display_name_with_location
from problem_events
