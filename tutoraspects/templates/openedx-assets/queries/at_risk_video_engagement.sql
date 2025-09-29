select distinct
    video.org as org,
    video.course_key as course_key,
    video.section_subsection_name as section_subsection_name,
    video.content_level as content_level,
    video.actor_id as actor_id,
    video.section_subsection_video_engagement as section_subsection_video_engagement,
    video.block_id as block_id,
    users.username as username,
    users.name as name,
    users.email as email
from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_video_engagement video
left join
    {{ ASPECTS_EVENT_SINK_DATABASE }}.user_pii users
    on (video.actor_id like 'mailto:%' and SUBSTRING(actor_id, 8) = users.email)
    or video.actor_id = toString(users.external_user_id)
join
    (
        {% include 'openedx-assets/queries/at_risk_learner_filter.sql' %}
    ) as at_risk_learners using (org, course_key, actor_id)
where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
