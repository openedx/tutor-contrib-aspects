select
    org,
    course_key,
    course_name,
    course_run,
    actor_id,
    count(*) as num_posts
from
    {{ DBT_PROFILE_TARGET_DATABASE }}.fact_forum_interactions
where
    1=1
    {% raw %}
    {% if from_dttm is not none %}
    and emission_time > '{{ from_dttm }}'
    {% endif %}
    {% if to_dttm is not none %}
    and emission_time < '{{ to_dttm }}'
    {% endif %}
    {% endraw %}
group by
    org,
    course_key,
    course_name,
    course_run,
    actor_id
