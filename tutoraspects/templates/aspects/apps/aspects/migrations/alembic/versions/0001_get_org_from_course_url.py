from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """
    -- Create the terrible user defined function to parse the org out of course URLs
    -- if we need to update this just add a COALESCE around the whole thing and put in
    -- additional cases wrapped in nullIf's until we get them all. Other things we may find in these URLs eventually:
    -- i4x://{org}/{rest of key}  Old Mongo usage keys
    -- c4x://{org}/{rest of key}  Old Mongo assets
    -- {org}/{rest of key} Old Mongo course keys
    """
    op.execute(
        f"""
        CREATE OR REPLACE FUNCTION get_org_from_course_url
        AS (
        course_url) ->
        nullIf(EXTRACT(course_url, 'course-v1:([a-zA-Z0-9]*)'), '');
        """
    )


def downgrade():
    op.execute(f"DROP FUNCTION IF EXISTS get_org_from_course_url;")
