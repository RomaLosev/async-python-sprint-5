"""01_initial-db

Revision ID: ae2aa16912d0
Revises: 
Create Date: 2022-10-30 15:20:05.720404

"""
import sqlalchemy as sa
from alembic import op
from fastapi_users_db_sqlalchemy import GUID

# revision identifiers, used by Alembic.
revision = 'ae2aa16912d0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('files',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('path', sa.String(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('is_downloadable', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_files_created_at'), 'files', ['created_at'], unique=False)
    op.create_table('user',
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('id', GUID(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_files_created_at'), table_name='files')
    op.drop_table('files')
    # ### end Alembic commands ###
