"""
This migration handles the somewhat complicated action of changing the table engine
for the Vector xAPI table from MergeTree to ReplacingMergeTree. It takes a few steps.
"""
from alembic import op
import sqlalchemy as sa

revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None

DESTINATION_TABLE = "{{ ASPECTS_XAPI_DATABASE }}.{{ ASPECTS_XAPI_TABLE }}"
TMP_TABLE_NEW = f"{DESTINATION_TABLE}_tmp_{revision}"
TMP_TABLE_ORIG = f"{DESTINATION_TABLE}_tmp_mergetree_{revision}"


def upgrade():
    # 1. Create our new table with the desired engine
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
            emission_time DateTime64(6),
            event_str     String
        )
        ENGINE = ReplacingMergeTree 
        PRIMARY KEY (org, course_id, verb_id, actor_id, emission_time, event_id)
        ORDER BY (org, course_id, verb_id, actor_id, emission_time, event_id);
        """
    )
    # 2. Attach our table to the existing partitions of the old MergeTree table.
    #    This works because our "order by" is the same. It should be instant no matter
    #    the size of the table since it's not copying anything.
    op.execute(
        f"""
        ALTER TABLE {TMP_TABLE_NEW}
        ATTACH PARTITION tuple() FROM 
        {DESTINATION_TABLE}
        """
    )
    # 3. Swap both tables in a single rename statement.
    op.execute(
        f"""
        RENAME TABLE {DESTINATION_TABLE} 
         TO {TMP_TABLE_ORIG}, 
         {TMP_TABLE_NEW}
         TO {DESTINATION_TABLE};
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
    # 2. Attach our table to the existing partitions of the ReplacingMergeTree table.
    #    This works because our "order by" is the same. It should be instant no matter
    #    the size of the table since it's not copying anything.
    op.execute(
        f"""
        ALTER TABLE {TMP_TABLE_ORIG}
        ATTACH PARTITION tuple() FROM 
        {DESTINATION_TABLE};
        """
    )
    # 3. Swap both tables in a single rename statement.
    op.execute(
        f"""
        RENAME TABLE {DESTINATION_TABLE}
         TO {TMP_TABLE_NEW}, 
         {TMP_TABLE_ORIG}
         TO {DESTINATION_TABLE};
        """
    )
    # 4. Force deduplication of the existing data and may take a very long time
    #    on a larger dataset, but since Aspects isn't in production anywhere yet this
    #    seems like a reasonable thing to do. If you're looking at this as fodder for
    #    a future migration, make sure to understand the potential issues here.
    op.execute(
        f"""
        OPTIMIZE TABLE {DESTINATION_TABLE} 
        FINAL DEDUPLICATE;
        """
    )
    # 5. Drop the renamed version of the original table.
    op.execute(
        f"""
        DROP TABLE {TMP_TABLE_NEW};
        """
    )
