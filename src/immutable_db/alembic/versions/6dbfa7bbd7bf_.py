"""empty message

Revision ID: 6dbfa7bbd7bf
Revises: a3f6b21dc87f
Create Date: 2023-02-14 06:03:22.812868

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "6dbfa7bbd7bf"
down_revision = "a3f6b21dc87f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "application",
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_table(
        "application_user",
        sa.Column("application_uuid", sa.UUID(), nullable=False),
        sa.Column("user_uuid", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["application_uuid"],
            ["application.uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["user_uuid"],
            ["user.uuid"],
        ),
        sa.PrimaryKeyConstraint("application_uuid", "user_uuid"),
    )


def downgrade() -> None:
    op.drop_table("application_user")
    op.drop_table("application")
