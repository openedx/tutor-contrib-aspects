"""Update the get org function to include other characters"""
from alembic import op
import sqlalchemy as sa

revision = "0020"
down_revision = "0019"
branch_labels = None
depends_on = None
on_cluster = " ON CLUSTER '{{CLICKHOUSE_CLUSTER_NAME}}' " if "{{CLICKHOUSE_CLUSTER_NAME}}" else ""


def upgrade():
    op.execute(
        f"""
        CREATE OR REPLACE FUNCTION get_org_from_course_url {on_cluster}
        AS (
        course_url) ->
        nullIf(EXTRACT(course_url, 'course-v1:([a-zA-Z0-9\w\-~.:%]*)'), '');
        """
    )


def downgrade():
    op.execute(
        f"""
        CREATE OR REPLACE FUNCTION get_org_from_course_url {on_cluster}
        AS (
        course_url) ->
        nullIf(EXTRACT(course_url, 'course-v1:([a-zA-Z0-9]*)'), '');
        """
    )
