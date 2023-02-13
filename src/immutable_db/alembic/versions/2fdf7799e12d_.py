"""empty message

Revision ID: 2fdf7799e12d
Revises: e3a577eed6fc
Create Date: 2023-02-13 15:16:44.926984

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "2fdf7799e12d"
down_revision = "e3a577eed6fc"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("user", "deleted_at")


def downgrade() -> None:
    op.add_column(
        "user",
        sa.Column(
            "deleted_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
    )
