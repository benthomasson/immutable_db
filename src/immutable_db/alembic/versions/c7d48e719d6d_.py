"""empty message

Revision ID: c7d48e719d6d
Revises: 56d1ee61890a
Create Date: 2023-02-14 21:05:04.425088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c7d48e719d6d'
down_revision = '56d1ee61890a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('deleted_application_user_application_uuid_fkey', 'deleted_application_user', type_='foreignkey')
    op.drop_constraint('deleted_application_user_user_uuid_fkey', 'deleted_application_user', type_='foreignkey')
    op.drop_constraint('deleted_user_name_user_uuid_fkey', 'deleted_user_name', type_='foreignkey')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key('deleted_user_name_user_uuid_fkey', 'deleted_user_name', 'deleted_user', ['user_uuid'], ['uuid'])
    op.create_foreign_key('deleted_application_user_user_uuid_fkey', 'deleted_application_user', 'deleted_user', ['user_uuid'], ['uuid'])
    op.create_foreign_key('deleted_application_user_application_uuid_fkey', 'deleted_application_user', 'deleted_application', ['application_uuid'], ['uuid'])
    # ### end Alembic commands ###