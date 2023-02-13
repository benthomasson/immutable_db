"""empty message

Revision ID: b5921c11347d
Revises: de55144a38a0
Create Date: 2023-02-13 15:42:32.653543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5921c11347d'
down_revision = 'de55144a38a0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_constraint('user_name_user_uuid_fkey', 'user_name', type_='foreignkey')
    op.create_foreign_key(None, 'user_name', 'user', ['user_uuid'], ['uuid'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint(None, 'user_name', type_='foreignkey')
    op.create_foreign_key('user_name_user_uuid_fkey', 'user_name', 'user', ['user_uuid'], ['uuid'])
