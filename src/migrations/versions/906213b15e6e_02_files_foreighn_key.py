"""02_files_foreighn_key

Revision ID: 906213b15e6e
Revises: 983ac0cd9518
Create Date: 2022-10-30 17:30:29.496261

"""
import sqlalchemy as sa
from alembic import op
from fastapi_users_db_sqlalchemy import GUID

# revision identifiers, used by Alembic.
revision = '906213b15e6e'
down_revision = '983ac0cd9518'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('author', GUID(), nullable=True))
    op.create_foreign_key(None, 'files', 'user', ['author'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'files', type_='foreignkey')
    op.drop_column('files', 'author')
    # ### end Alembic commands ###
