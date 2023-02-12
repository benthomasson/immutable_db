"""empty message

Revision ID: 158339fde10b
Revises: 
Create Date: 2023-02-12 13:44:43.715941

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "158339fde10b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("uuid", sa.UUID(), nullable=False),
        sa.PrimaryKeyConstraint("uuid"),
    )


def downgrade() -> None:
    op.drop_table("user")
