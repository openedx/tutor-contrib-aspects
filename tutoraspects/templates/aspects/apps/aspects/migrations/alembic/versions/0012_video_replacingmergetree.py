from alembic import op
import sqlalchemy as sa

revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None

DESTINATION_TABLE = "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_VIDEO_PLAYBACK_EVENTS_TABLE }}"
TMP_TABLE_NEW = f"{DESTINATION_TABLE}_tmp_{revision}"
TMP_TABLE_ORIG = f"{DESTINATION_TABLE}_tmp_mergetree_{revision}"


def upgrade():
    # 1. Create our new table with the desired engine
    op.execute(
        f"""
        CREATE OR REPLACE TABLE {TMP_TABLE_NEW} (
            `event_id` UUID NOT NULL,
            `emission_time` DateTime64(6) NOT NULL,
            `actor_id` String NOT NULL,
            `object_id` String NOT NULL,
            `course_id` String NOT NULL,
            `org` String NOT NULL,
            `verb_id` LowCardinality(String) NOT NULL,
            `video_position` Float32 NOT NULL
        ) ENGINE = ReplacingMergeTree
        PRIMARY KEY (org, course_id, verb_id)
        ORDER BY (org, course_id, verb_id, actor_id, object_id, emission_time);
        """
    )
    # 2. Swap both tables in a single rename statement.
    op.execute(
        f"""
        RENAME TABLE {DESTINATION_TABLE} 
         TO {TMP_TABLE_ORIG}, 
         {TMP_TABLE_NEW}
         TO {DESTINATION_TABLE};
        """
    )
    # 3. Copy the contents of the old table to the new one. We can't just attach
    #    the old volume here because we're changing the ORDER BY to allow the
    #    replacement to work. This step can take a long time because of this.
    op.execute(
        f"""
        INSERT INTO {DESTINATION_TABLE} 
        SELECT * FROM {TMP_TABLE_ORIG};
        """
    )
    # 4. Force deduplication of the existing data and may take a very long time
    #    on a larger dataset, but since Aspects isn't in production anywhere yet this
    #    seems like a reasonable thing to do. If you're looking at this as fodder for
    #    a future migration, make sure to understand the potential issues here.
    op.execute(
        f"""
        OPTIMIZE TABLE {DESTINATION_TABLE} FINAL;
        """
    )
    # 5. Drop the renamed version of the original table.
    op.execute(
        f"""
        DROP TABLE {TMP_TABLE_ORIG};
        """
    )


def downgrade():
    # 1. Create a new table with the old engine
    op.execute(
        f"""
        CREATE OR REPLACE TABLE {TMP_TABLE_ORIG} (
            `event_id` UUID NOT NULL,
            `emission_time` DateTime64(6) NOT NULL,
            `actor_id` String NOT NULL,
            `object_id` String NOT NULL,
            `course_id` String NOT NULL,
            `org` String NOT NULL,
            `verb_id` LowCardinality(String) NOT NULL,
            `video_position` Float32 NOT NULL
        ) ENGINE = MergeTree
        PRIMARY KEY (org, course_id, verb_id)
        ORDER BY (org, course_id, verb_id, actor_id);
        """
    )
    # 2. Swap both tables in a single rename statement.
    op.execute(
        f"""
        RENAME TABLE {DESTINATION_TABLE}
         TO {TMP_TABLE_NEW}, 
         {TMP_TABLE_ORIG}
         TO {DESTINATION_TABLE};
        """
    )
    # 3. Copy the contents of the old table to the new one. We can't just attach
    #    the old volume here because we're changing the ORDER BY to allow the
    #    replacement to work.
    op.execute(
        f"""
        INSERT INTO {DESTINATION_TABLE} 
        SELECT * FROM {TMP_TABLE_NEW};
        """
    )
    # 4. In some other downgrades from ReplacingMergeTree to MergeTree we do an
    #    "optimize deduplicate" operation here. However, we're changing the sort order
    #    in this migration, and the original sort order is not granular enough to
    #    support deduplication without losing rows, so we do not do that here.
    #
    # 5. Drop the renamed version of the original table.
    op.execute(
        f"""
        DROP TABLE {TMP_TABLE_NEW};
        """
    )
