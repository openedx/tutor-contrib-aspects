select
    org,
    course_name,
    course_key,
    course_run,
    block_id as video_id,
    block_name as video_name,
    display_name_with_location as video_name_with_location
from
    {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks
where
    video_id like '%video+block%'
{% raw -%}
    {% if filter_values('org') != [] %}
    and org in {{ filter_values('org') | where_in }}
    {% endif %}
    {% if filter_values('video_name_with_location') != [] %}
    and video_name_with_location in {{ filter_values('video_name_with_location') | where_in }}
    {% endif %}
{%- endraw %}
