with enrollments_ranked as (
  select
    emission_time,
    org,
    course_key,
    course_name,
    course_run,
    actor_id,
    enrollment_mode,
    enrollment_status,
    rank() over (partition by date(emission_time), org, course_name, course_run, actor_id order by emission_time desc) as event_rank
  from {{ DBT_PROFILE_TARGET_DATABASE }}.fact_enrollments
  where
    1=1
    {% include 'openedx-assets/queries/common_filters.sql' %}
), enrollment_windows as (
  select
    org,
    course_key,
    course_name,
    course_run,
    actor_id,
    enrollment_status,
    enrollment_mode,
    date_trunc('day', emission_time) as window_start_date,
    date_trunc('day', lagInFrame(emission_time, 1, now() + interval '1' day) over (partition by org, course_name, course_run, actor_id order by emission_time desc)) as window_end_date
  from
    enrollments_ranked
  where
    event_rank = 1
)
select
    date(fromUnixTimestamp(
        arrayJoin(
            range(
                toUnixTimestamp(window_start_date),
                toUnixTimestamp(window_end_date),
                86400
            )
        )
    )) as enrollment_status_date,
    org,
    course_key,
    course_name,
    course_run,
    actor_id,
    enrollment_status,
    enrollment_mode
from enrollment_windows
