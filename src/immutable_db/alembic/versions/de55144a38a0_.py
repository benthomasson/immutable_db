"""empty message

Revision ID: de55144a38a0
Revises: 2fdf7799e12d
Create Date: 2023-02-13 15:34:10.318367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de55144a38a0'
down_revision = '2fdf7799e12d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('deleted_user_name',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.Column('user_uuid', sa.UUID(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['user_uuid'], ['deleted_user.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('user_name',
    sa.Column('uuid', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('user_uuid', sa.UUID(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['user_uuid'], ['user.uuid'], ),
    sa.PrimaryKeyConstraint('uuid')
    )


def downgrade() -> None:
    op.drop_table('user_name')
    op.drop_table('deleted_user_name')
