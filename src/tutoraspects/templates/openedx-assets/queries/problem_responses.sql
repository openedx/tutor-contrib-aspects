select
    responses.emission_time as emission_time,
    responses.org as org,
    responses.course_key as course_key,
    toFloat32OrNull(responses.response) as response_numeric,
    toString(responses.response) as response_string,
    if(responses.success, 'Correct', 'Incorrect') as success,
    responses.interaction_type as interaction_type,
    responses.problem_number as problem_number,
    responses.problem_name_location as problem_name_location,
    responses.block_id_short as block_id,
    responses.response_count as response_count,
    concat('#', splitByString('_', responses.problem_number)[2]) as problem_part
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_problem_responses responses
