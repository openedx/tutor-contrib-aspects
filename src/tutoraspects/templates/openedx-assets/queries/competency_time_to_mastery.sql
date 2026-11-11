-- Time to mastery of every demonstrated learner x competency, once per time unit,
-- so a single-select "Time unit" filter on time_unit picks the unit the box plot
-- shows. Superset's time grain only applies to a time axis, not to a measured
-- duration.
select
    org,
    course_key,
    course_name,
    actor_id,
    tag_id,
    competency,
    competency_path,
    competency_level,
    status,
    unit.1 as time_unit,
    time_to_mastery_seconds / unit.2 as time_to_mastery,
    time_to_mastery_seconds,
    -- Zero-padded so the buckets sort in time order.
    multiIf(
        time_to_mastery_seconds < 86400, '00-01 days',
        time_to_mastery_seconds < 3 * 86400, '01-03 days',
        time_to_mastery_seconds < 7 * 86400, '03-07 days',
        time_to_mastery_seconds < 14 * 86400, '07-14 days',
        time_to_mastery_seconds < 28 * 86400, '14-28 days',
        '28+ days'
    ) as time_to_mastery_bucket
from (
    {% include 'openedx-assets/queries/competency_learner_status.sql' %}
) as learner_status
array join
    [('Hours', 3600), ('Days', 86400), ('Weeks', 604800), ('Months', 2629800)] as unit
where mastered_at is not null
