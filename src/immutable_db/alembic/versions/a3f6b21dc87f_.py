"""empty message

Revision ID: a3f6b21dc87f
Revises: b5921c11347d
Create Date: 2023-02-13 17:50:43.911504

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a3f6b21dc87f'
down_revision = 'b5921c11347d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('deleted_user', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('deleted_user', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('deleted_user_name', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('deleted_user_name', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('deleted_user_name', 'user_uuid',
               existing_type=sa.UUID(),
               nullable=False)
    op.alter_column('user', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('user_name', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('user_name', 'user_uuid',
               existing_type=sa.UUID(),
               nullable=False)


def downgrade() -> None:
    op.alter_column('user_name', 'user_uuid',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('user_name', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('user', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('deleted_user_name', 'user_uuid',
               existing_type=sa.UUID(),
               nullable=True)
    op.alter_column('deleted_user_name', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('deleted_user_name', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('deleted_user', 'deleted_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('deleted_user', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
