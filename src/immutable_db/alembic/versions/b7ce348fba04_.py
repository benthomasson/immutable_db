"""empty message

Revision ID: b7ce348fba04
Revises: 6dbfa7bbd7bf
Create Date: 2023-02-14 06:05:45.680240

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "b7ce348fba04"
down_revision = "6dbfa7bbd7bf"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "deleted_application",
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_table(
        "deleted_application_user",
        sa.Column("application_uuid", sa.UUID(), nullable=False),
        sa.Column("user_uuid", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["application_uuid"],
            ["deleted_application.uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["user_uuid"],
            ["deleted_user.uuid"],
        ),
        sa.PrimaryKeyConstraint("application_uuid", "user_uuid"),
    )


def downgrade() -> None:
    op.drop_table("deleted_application_user")
    op.drop_table("deleted_application")
