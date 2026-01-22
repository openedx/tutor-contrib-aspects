select
    emission_time,
    org,
    course_key,
    toFloat32OrNull(response) as response_numeric,
    toString(response) as response_string,
    if(success, 'Correct', 'Incorrect') as success,
    interaction_type,
    problem_number,
    problem_name_location,
    block_id_short as block_id,
    response_count,
    concat('#', splitByString('_', problem_number)[2]) as problem_part
from {{ DBT_PROFILE_TARGET_DATABASE }}.dim_problem_responses
