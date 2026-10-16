with
    watches as (
        select
            org,
            course_key,
            actor_id,
            object_id,
            video_duration,
            watched_seconds,
            max_views
        from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_video_watches final
        where 1 = 1 {% include 'openedx-assets/queries/common_filters.sql' %}
    ),
    final_results as (
        select
            watches.org as org,
            watches.course_key as course_key,
            arrayStringConcat(
                arrayMap(
                    x -> (leftPad(x, 2, char(917768))),
                    splitByString(
                        ':', splitByString(' - ', blocks.display_name_with_location)[1]
                    )
                ),
                ':'
            ) as video_number,
            concat(
                video_number,
                ' - ',
                splitByString(' - ', blocks.display_name_with_location)[2]
            ) as video_name_location,
            concat(
                '<a href="',
                watches.object_id,
                '" target="_blank">',
                video_name_location,
                '</a>'
            ) as video_link,
            watches.actor_id as actor_id,
            users.username as username,
            users.email as email,
            users.name as name,
            watches.max_views as video_watched_count,
            if(watches.max_views > 1, watches.max_views, 0) as video_rewatched_count,
            watches.watched_seconds / watches.video_duration
            >= .95 as watched_entire_video,
            blocks.section_with_name as section_with_name,
            blocks.subsection_with_name as subsection_with_name
        from watches
        join
            {{ DBT_PROFILE_TARGET_DATABASE }}.dim_course_blocks blocks
            on (
                watches.course_key = blocks.course_key
                and splitByString('/xblock/', watches.object_id)[-1] = blocks.block_id
            )
        left outer join
            {{ DBT_PROFILE_TARGET_DATABASE }}.dim_user_pii users
            on (
                watches.actor_id like 'mailto:%'
                and SUBSTRING(watches.actor_id, 8) = users.email
            )
            or watches.actor_id = toString(users.external_user_id)
    )
select
    org,
    course_key,
    video_name_location,
    video_link,
    actor_id,
    username,
    email,
    name,
    video_watched_count,
    video_rewatched_count,
    watched_entire_video,
    section_with_name,
    subsection_with_name
from final_results
