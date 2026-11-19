from alembic import op

revision = "0045"
down_revision = "0044"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""


def upgrade():
    # "competency" for a taxonomy backed by an openedx-core CompetencyTaxonomy row,
    # "tags" otherwise, as platform-plugin-aspects' TaxonomySink serializes it.
    # Sink inserts are positional CSV, so the column goes last, after
    # time_last_dumped, matching the serializer's field order. Rows dumped before
    # this column existed read as "tags" until the taxonomy is dumped again
    # (dump_data_to_clickhouse --object taxonomy --force).
    op.execute(
        f"""
        ALTER TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.taxonomy
        {on_cluster}
        ADD COLUMN IF NOT EXISTS taxonomy_type LowCardinality(String) DEFAULT 'tags';
        """
    )


def downgrade():
    # ClickHouse refuses to drop a column a materialized view reads, and aspects-dbt's
    # dim_most_recent_taxonomies selects taxonomy_type. Drop its view first, as 0029 does;
    # set DBT_BRANCH back to an aspects-dbt release before v9.0.0 so the next dbt run
    # recreates it without taxonomy_type; v9.0.0+ fails against the downgraded table.
    op.execute(
        f"""
        DROP VIEW IF EXISTS {{ ASPECTS_EVENT_SINK_DATABASE }}.dim_most_recent_taxonomies_mv
        {on_cluster};
        """
    )
    op.execute(
        f"""
        ALTER TABLE {{ ASPECTS_EVENT_SINK_DATABASE }}.taxonomy
        {on_cluster}
        DROP COLUMN IF EXISTS taxonomy_type;
        """
    )
