from alembic import op

revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None

DESTINATION_TABLE = "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}"
TMP_TABLE_NEW = f"{DESTINATION_TABLE}_tmp_{revision}"
TMP_TABLE_ORIG = f"{DESTINATION_TABLE}_tmp_mergetree_{revision}"


def upgrade():
    # 1. Create our new temp table with the desired changes
    op.execute(
        f"""
        CREATE OR REPLACE TABLE {TMP_TABLE_NEW}
        (
            event_id      UUID,
            verb_id       String,
            actor_id      String,
            object_id     String,
            org           String,
            course_id     String,
            emission_time DateTime,
            event_str     String
        )
        ENGINE = ReplacingMergeTree 
        PRIMARY KEY (org, course_id, emission_time, verb_id, actor_id, event_id)
        ORDER BY (org, course_id, emission_time, verb_id, actor_id, event_id);
        """
    )
    # 2. Swap both tables in a single rename statement. New data will flow into
    #    the new table now and cascade through the MVs and downstream tables per normal.
    op.execute(
        f"""
        RENAME TABLE {DESTINATION_TABLE} 
         TO {TMP_TABLE_ORIG}, 
         {TMP_TABLE_NEW}
         TO {DESTINATION_TABLE};
        """
    )
    # 3. Copy in all existing rows from the parent raw table. This will cascade through
    #    the system and duplicate rows downstream, but the alternative is to potentially
    #    lose rows in this table while performing a copy. Downstream tables at this
    #    point are all ReplacingMergeTree, we will force them all do dedupe at the end.
    #
    #    This is the SQL from the current version of the materialized view that
    #    populates this table.
    op.execute(
        f"""
        INSERT INTO {DESTINATION_TABLE}
        SELECT
        event_id as event_id,
        JSON_VALUE(event_str, '$.verb.id') as verb_id,
        COALESCE(
            NULLIF(JSON_VALUE(event_str, '$.actor.account.name'), ''),
            NULLIF(JSON_VALUE(event_str, '$.actor.mbox'), ''),
            JSON_VALUE(event_str, '$.actor.mbox_sha1sum')
        ) as actor_id,
        JSON_VALUE(event_str, '$.object.id') as object_id,
        if(
            JSON_VALUE(
                event_str,
                '$.context.contextActivities.parent[0].definition.type')
                    = 'http://adlnet.gov/expapi/activities/course',
                JSON_VALUE(event_str, '$.context.contextActivities.parent[0].id'),
                JSON_VALUE(event_str, '$.object.id')
            ) as course_id,
        get_org_from_course_url(course_id) as org,
        emission_time as emission_time,
        event_str as event_str
        FROM {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }};
        """
    )
    # 5. Force deduplication of the existing data. This may take a very long time
    #    on a larger dataset, but since Aspects isn't in production anywhere yet this
    #    seems like a reasonable thing to do. If you're looking at this as fodder for
    #    a future migration, make sure to understand the potential issues here.
    optimize()

    # 6. Drop the renamed version of the original table.
    op.execute(
        f"""
        DROP TABLE {TMP_TABLE_ORIG};
        """
    )


def downgrade():
    # 1. Create a new table with the old engine
    op.execute(
        f"""
        CREATE OR REPLACE TABLE {TMP_TABLE_ORIG}
        (
            event_id      UUID,
            verb_id       String,
            actor_id      String,
            object_id     String,
            org           String,
            course_id     String,
            emission_time DateTime64(6),
            event_str     String
        )
        ENGINE = MergeTree 
        PRIMARY KEY (org, course_id, verb_id, actor_id, emission_time, event_id)
        ORDER BY (org, course_id, verb_id, actor_id, emission_time, event_id);
        """
    )
    # 2. Swap both tables in a single rename statement. New data will flow into
    #    the new table now and cascade through the MVs and downstream tables per normal.
    op.execute(
        f"""
        RENAME TABLE {DESTINATION_TABLE} 
         TO {TMP_TABLE_NEW}, 
         {TMP_TABLE_ORIG}
         TO {DESTINATION_TABLE};
        """
    )
    # 3. Copy in all existing rows from the parent raw table. This will cascade through
    #    the system and duplicate rows downstream, but the alternative is to potentially
    #    lose rows in this table while performing a copy. Downstream tables at this
    #    point are all ReplacingMergeTree, we will force them all do dedupe at the end.
    #
    #    This is the SQL from the current version of the materialized view that
    #    populates this table.
    op.execute(
        f"""
        INSERT INTO {DESTINATION_TABLE}
        SELECT
        event_id as event_id,
        JSON_VALUE(event_str, '$.verb.id') as verb_id,
        COALESCE(
            NULLIF(JSON_VALUE(event_str, '$.actor.account.name'), ''),
            NULLIF(JSON_VALUE(event_str, '$.actor.mbox'), ''),
            JSON_VALUE(event_str, '$.actor.mbox_sha1sum')
        ) as actor_id,
        JSON_VALUE(event_str, '$.object.id') as object_id,
        if(
            JSON_VALUE(
                event_str,
                '$.context.contextActivities.parent[0].definition.type')
                    = 'http://adlnet.gov/expapi/activities/course',
                JSON_VALUE(event_str, '$.context.contextActivities.parent[0].id'),
                JSON_VALUE(event_str, '$.object.id')
            ) as course_id,
        get_org_from_course_url(course_id) as org,
        emission_time as emission_time,
        event_str as event_str
        FROM {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_RAW_XAPI_TABLE }};
        """
    )
    # 5. Force deduplication of the existing data. This may take a very long time
    #    on a larger dataset, but since Aspects isn't in production anywhere yet this
    #    seems like a reasonable thing to do. If you're looking at this as fodder for
    #    a future migration, make sure to understand the potential issues here.
    optimize()

    # 6. Drop the renamed version of the original table.
    op.execute(
        f"""
        DROP TABLE {TMP_TABLE_NEW};
        """
    )


def optimize():
    op.execute(
        f"""
        OPTIMIZE TABLE {DESTINATION_TABLE} FINAL;
        """
    )
    op.execute(
        f"""
        OPTIMIZE TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_ENROLLMENT_EVENTS_TABLE }}
        FINAL;
        """
    )
    op.execute(
        f"""
        OPTIMIZE TABLE 
        {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE }}
        FINAL;
        """
    )
    op.execute(
        f"""
        OPTIMIZE TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_PROBLEM_EVENTS_TABLE }}
        FINAL;
        """
    )
    op.execute(
        f"""
        OPTIMIZE TABLE {{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_NAVIGATION_EVENTS_TABLE }}
        FINAL;
        """
    )
