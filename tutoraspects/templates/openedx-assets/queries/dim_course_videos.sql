select
    org,
    course_name,
    course_key,
    course_run,
    block_id as video_id,
    block_name as video_name
from
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks
where
    video_id like '%video+block%'
{% raw -%}
    {% if filter_values('org') != [] %}
    and org in {{ filter_values('org') | where_in }}
    {% endif %}
    {% if filter_values('video_name') != [] %}
    and video_name in {{ filter_values('video_name') | where_in }}
    {% endif %}
{%- endraw %}
