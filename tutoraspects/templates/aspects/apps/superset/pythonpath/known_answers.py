"""
Check chart numbers against the known answers of the learner journeys test data.

``tutor [local|dev|k8s] do load-xapi-test-data`` loads learner journeys whose expected results
are in the ``journeys`` database. This runs the engagement and video charts through Superset,
the same way a dashboard does, once per journeys course, and compares every bar with the expected
results. It exits non-zero if any number differs, so a change in xapi-db-load, aspects-dbt or the
Superset datasets that changes what the charts show is caught.
"""
import copy
import logging
import sys
import unicodedata
from collections import defaultdict

import click
import clickhouse_connect

from performance_metrics import (
    get_query_contexts_from_assets,
    get_slice_query_context,
    measure_chart,
)
from superset.extensions import db
from superset.models.slice import Slice

logger = logging.getLogger("known_answers")

EXPECTED_DB = "journeys"
EVENT_SINK_DB = "{{ASPECTS_EVENT_SINK_DATABASE}}"

# Bar charts of learners per section and subsection: (chart uuid, metric, "at least one" and
# "all" metric names).
ENGAGEMENT_CHARTS = [
    ("bf2d6219-d633-48c1-a9b5-742eac6a4c0a", "pages",
     "at_leat_one_page_viewed", "all_pages_viewed"),
    ("8cdcd4aa-1fa2-41dc-b38d-f1112134592e", "problems",
     "attempted_at_least_one_problem", "attempted_all_problems"),
    ("c1f77432-e55f-4473-b7d0-7a1c3976e6a8", "videos",
     "at_least_one_viewed", "all_videos_viewed"),
]
# Bar charts of views per video: (chart uuid, {chart metric: expected column}).
VIDEO_CHARTS = [
    ("ace4c769-00f4-4708-887b-14fd9e5f384e",
     {"Total Views": "total_views", "Repeat Views": "repeat_views"}),
    ("bfffb9fe-07bd-4b2f-b437-522d45f6cd2c",
     {"full_views": "full_views", "partial_views": "partial_views"}),
]
# Views per second of video: the bars add up to every second watched, rewatches included.
SEGMENTS_CHART = "2985a9db-c338-4008-af52-2930b81ee2e5"

# EXPECTED_DB, EVENT_SINK_DB and COURSE_KEY are replaced before each query runs.
NAMES_SQL = """
    select location, display_name_with_location as name
    from EVENT_SINK_DB.dim_most_recent_course_blocks
    where course_key = COURSE_KEY
"""
EXPECTED_ENGAGEMENT_SQL = """
    select e.metric, n.name,
        countIf(e.status like 'At least%' or e.status like 'All%') as at_least,
        countIf(e.status like 'All%') as all
    from EXPECTED_DB.expected_engagement e
    join (NAMES_SQL) n on n.location = e.block_id
    where e.course_key = COURSE_KEY
    group by e.metric, n.name
""".replace("NAMES_SQL", NAMES_SQL)
EXPECTED_VIDEO_SQL = """
    select n.name,
        sum(e.observable_max_views) as total_views,
        sum(if(e.observable_max_views > 1, e.observable_max_views, 0)) as repeat_views,
        sumIf(e.observable_max_views,
              e.observable_distinct_seconds / e.video_duration >= 0.95) as full_views,
        sumIf(e.observable_max_views,
              e.observable_distinct_seconds / e.video_duration < 0.95) as partial_views,
        sum(e.observable_seconds) as seconds
    from EXPECTED_DB.expected_video_seconds e
    join (NAMES_SQL) n on n.location = e.video_block_id
    where e.course_key = COURSE_KEY
    group by n.name
""".replace("NAMES_SQL", NAMES_SQL)


def sql(template, course_key=""):
    """Fill in the database names and a quoted course key."""
    quoted = "'" + course_key.replace("\\", "\\\\").replace("'", "\\'") + "'"
    return (
        template.replace("EXPECTED_DB", EXPECTED_DB)
        .replace("EVENT_SINK_DB", EVENT_SINK_DB)
        .replace("COURSE_KEY", quoted)
    )


def clickhouse():
    """Return a ClickHouse client that can read the expected results."""
    return clickhouse_connect.get_client(
        host="{{CLICKHOUSE_HOST}}",
        port=int("{{CLICKHOUSE_INTERNAL_HTTP_PORT}}"),
        username="{{CLICKHOUSE_ADMIN_USER}}",
        password="{{CLICKHOUSE_ADMIN_PASSWORD}}",
        secure={{CLICKHOUSE_SECURE_CONNECTION}},
    )


def video_key(name):
    """
    Return "<location> - <name>" for a video, without the padding characters the video_watches
    dataset adds to the location so videos sort in course order.
    """
    name = "".join(c for c in str(name) if unicodedata.category(c)[0] not in "CM")
    return " - ".join(name.split(" - ")[:2])


def run_chart(uuid, course_key, query_contexts):
    """Run a chart for one course and return its rows, before any pivoting."""
    chart = db.session.query(Slice).filter(Slice.uuid == uuid).one()
    # get_slice_query_context changes the context it's given, so give it a copy per run.
    query_context = get_slice_query_context(
        chart, {uuid: copy.deepcopy(query_contexts[uuid])}
    )
    for query in query_context["queries"]:
        query["post_processing"] = []
        query["row_limit"] = 100000
        query["filters"] = query.get("filters", []) + [
            {"col": "course_key", "op": "IN", "val": [course_key]}
        ]
    result = measure_chart(chart, query_context, fail_on_error=True)
    return chart.slice_name, result["queries"][0]["data"]


def compare(label, expected, actual, problems):
    """Record every key where the expected and actual numbers differ."""
    for key in sorted(set(expected) | set(actual)):
        width = len(next(iter(expected.values() or actual.values())))
        exp, act = expected.get(key, (0,) * width), actual.get(key, (0,) * width)
        if tuple(exp) != tuple(act):
            problems.append(f"{label}: {key!r}: expected {tuple(exp)}, chart shows {tuple(act)}")


def check_course(client, course_key, query_contexts):
    """Return the differences between the charts and the known answers for one course."""
    problems = []

    expected = defaultdict(dict)
    for metric, name, at_least, all_ in client.query(
        sql(EXPECTED_ENGAGEMENT_SQL, course_key)
    ).result_rows:
        expected[metric][name] = (at_least, all_)
    for uuid, metric, at_least_metric, all_metric in ENGAGEMENT_CHARTS:
        chart_name, rows = run_chart(uuid, course_key, query_contexts)
        actual = {
            r["section_subsection_name"]: (r[at_least_metric], r[all_metric])
            for r in rows if r["section_subsection_name"]
        }
        compare(f"{course_key} {chart_name}", expected[metric], actual, problems)

    videos = {}
    for row in client.query(sql(EXPECTED_VIDEO_SQL, course_key)).named_results():
        videos[video_key(row.pop("name"))] = row
    for uuid, metrics in VIDEO_CHARTS:
        chart_name, rows = run_chart(uuid, course_key, query_contexts)
        actual = {
            video_key(r["video_name_location"]): tuple(r[m] for m in metrics) for r in rows
        }
        exp = {
            k: tuple(v[c] for c in metrics.values())
            for k, v in videos.items() if any(v[c] for c in metrics.values())
        }
        compare(f"{course_key} {chart_name}", exp, actual, problems)

    chart_name, rows = run_chart(SEGMENTS_CHART, course_key, query_contexts)
    compare(
        f"{course_key} {chart_name}",
        {"seconds watched": (sum(v["seconds"] for v in videos.values()),)},
        {"seconds watched": (sum(r["total_views"] for r in rows),)},
        problems,
    )
    return problems


@click.command()
def known_answers():
    """Compare the engagement and video charts with the journeys known answers."""
    client = clickhouse()
    courses = [
        r[0] for r in client.query(
            sql("select distinct course_key from EXPECTED_DB.expected_engagement order by 1")
        ).result_rows
    ]
    if not courses:
        logger.error("No known answers found; run load-xapi-test-data first.")
        sys.exit(1)

    query_contexts = get_query_contexts_from_assets()
    problems = []
    for course_key in courses:
        course_problems = check_course(client, course_key, query_contexts)
        logger.info(f"{course_key}: {len(course_problems)} differences")
        problems += course_problems

    for problem in problems:
        logger.error(problem)
    if problems:
        logger.error(f"{len(problems)} chart numbers differ from the known answers.")
        sys.exit(1)
    logger.info(f"Every checked chart number matches the known answers for {len(courses)} courses.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    known_answers()
