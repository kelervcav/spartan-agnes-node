"""create user table

Revision ID: 41798222ba3f
Revises: 9a99eda0211c
Create Date: 2022-09-05 19:09:42.615465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41798222ba3f'
down_revision = '9a99eda0211c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('firstname', sa.String, nullable=False),
        sa.Column('lastname', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False)
    )


def downgrade() -> None:
    p.drop_table('users')
