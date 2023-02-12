"""empty message

Revision ID: e3a577eed6fc
Revises: 158339fde10b
Create Date: 2023-02-12 13:45:48.720843

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "e3a577eed6fc"
down_revision = "158339fde10b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "deleted_user",
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.add_column("user", sa.Column("created_at", sa.DateTime(), nullable=True))
    op.add_column("user", sa.Column("deleted_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("user", "deleted_at")
    op.drop_column("user", "created_at")
    op.drop_table("deleted_user")
