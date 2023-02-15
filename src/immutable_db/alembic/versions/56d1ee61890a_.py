"""empty message

Revision ID: 56d1ee61890a
Revises: b7ce348fba04
Create Date: 2023-02-14 06:25:37.297726

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "56d1ee61890a"
down_revision = "b7ce348fba04"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "application_user", sa.Column("created_at", sa.DateTime(), nullable=False)
    )
    op.add_column(
        "deleted_application_user",
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.add_column(
        "deleted_application_user",
        sa.Column("deleted_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_column("deleted_application_user", "deleted_at")
    op.drop_column("deleted_application_user", "created_at")
    op.drop_column("application_user", "created_at")
