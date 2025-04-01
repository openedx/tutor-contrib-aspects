with
    max_attempts as (
        select
            full_responses.org as org,
            full_responses.course_key as course_key,
            argMax(full_responses.success, full_responses.attempts) as success,
            actor_id,
            max(full_responses.attempts) as attempts,
            object_id,
            problem_id
        from {{ ASPECTS_XAPI_DATABASE }}.problem_events as full_responses
        group by org, course_key, actor_id, object_id, problem_id
    )
select
    org,
    course_key,
    splitByString('@', block_id)[-1] as block_id,
    actor_id,
    success,
    attempts,
    substring(
        regexpExtract(object_id, '(@problem\+block@[\w\d][^_\/]*)(_\d)?', 2), 2
    ) as _problem_id_number,
    cast(ifNull(nullIf(_problem_id_number, ''), '1') as Int) as _problem_id_or_1,
    splitByString(' - ', blocks.display_name_with_location)[1] as _problem_location,
    splitByString('-', blocks.display_name_with_location)[2] as _problem_name,
    if(
        blocks.display_name_with_location = '',
        '',
        concat(_problem_location, '(', _problem_id_or_1, ')', _problem_name)
    ) as problem_name_with_location,
    blocks.display_name_with_location
from max_attempts as full_responses
join
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks blocks
    on (
        full_responses.course_key = blocks.course_key
        and full_responses.problem_id = blocks.block_id
    )
