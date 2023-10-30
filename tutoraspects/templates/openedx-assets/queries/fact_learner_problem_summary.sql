WITH problem_responses AS (
        {% include 'openedx-assets/queries/int_problem_responses.sql' %}
), outcomes AS (
    SELECT
        emission_time,
        org,
        course_key,
        problem_id,
        actor_id,
        success,
        first_value(success) OVER (PARTITION BY course_key, problem_id, actor_id ORDER BY success ASC) AS was_successful
    FROM problem_responses
), successful_responses AS (
    SELECT
        org,
        course_key,
        problem_id,
        actor_id,
        min(emission_time) AS first_success_at
    FROM outcomes
    WHERE was_successful = true and success = true
    GROUP BY
        org,
        course_key,
        problem_id,
        actor_id
), unsuccessful_responses AS (
    SELECT
        org,
        course_key,
        problem_id,
        actor_id,
        max(emission_time) AS last_response_at
    FROM outcomes
    WHERE was_successful = false
    GROUP BY
        org,
        course_key,
        problem_id,
        actor_id
), final_responses AS (
    SELECT
        org,
        course_key,
        problem_id,
        actor_id,
        first_success_at AS emission_time
    FROM successful_responses
    UNION ALL
    SELECT
        org,
        course_key,
        problem_id,
        actor_id,
        last_response_at AS emission_time
    FROM unsuccessful_responses
), int_problem_results AS (
    SELECT
        emission_time,
        org,
        course_key,
        course_name,
        course_run,
        problem_id,
        problem_name,
        problem_name_with_location,
        actor_id,
        responses,
        success,
        attempts
    FROM problem_responses
    INNER JOIN final_responses USING (org, course_key, problem_id, actor_id, emission_time)
), summary AS (
    SELECT
        org,
        course_key,
        course_name,
        course_run,
        problem_name,
        problem_name_with_location,
        actor_id,
        success,
        attempts,
        0 AS num_hints_displayed,
        0 AS num_answers_displayed
    FROM int_problem_results
    UNION ALL
    SELECT
        org,
        course_key,
        course_name,
        course_run,
        problem_name,
        problem_name_with_location,
        actor_id,
        NULL AS success,
        NULL AS attempts,
        caseWithExpression(help_type, 'hint', 1, 0) AS num_hints_displayed,
        caseWithExpression(help_type, 'answer', 1, 0) AS num_answers_displayed
    FROM {{ DBT_PROFILE_TARGET_DATABASE }}.int_problem_hints
    WHERE
    1=1
    {% include 'openedx-assets/queries/common_filters.sql' %}
)

SELECT
    org,
    course_key,
    course_name,
    course_run,
    problem_name,
    problem_name_with_location,
    actor_id,
    coalesce(any(success), false) AS success,
    coalesce(any(attempts), 0) AS attempts,
    sum(num_hints_displayed) AS num_hints_displayed,
    sum(num_answers_displayed) AS num_answers_displayed
FROM summary
where
    {% raw %}
    {% if filter_values('problem_name_with_location') != [] %}
    problem_name_with_location in {{ filter_values('problem_name_with_location') | where_in }}
    {% else %}
    1=0
    {% endif %}
    {% endraw %}
GROUP BY
    org,
    course_key,
    course_name,
    course_run,
    problem_name,
    problem_name_with_location,
    actor_id
