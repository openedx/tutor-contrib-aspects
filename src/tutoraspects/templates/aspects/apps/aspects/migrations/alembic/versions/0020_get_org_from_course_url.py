"""Update the get org function to include other characters"""
from alembic import op
import sqlalchemy as sa

revision = "0020"
down_revision = "0017"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        f"""
        CREATE OR REPLACE FUNCTION get_org_from_course_url 
        AS (
        course_url) ->
        nullIf(EXTRACT(course_url, 'course-v1:([a-zA-Z0-9\\w\\-~.:%]*)'), '');
        """
    )


def downgrade():
    op.execute(
        f"""
        CREATE OR REPLACE FUNCTION get_org_from_course_url 
        AS (
        course_url) ->
        nullIf(EXTRACT(course_url, 'course-v1:([a-zA-Z0-9]*)'), '');
        """
    )
