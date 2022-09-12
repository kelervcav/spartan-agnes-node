"""create settings table

Revision ID: 9a99eda0211c
Revises: 42025c22e000
Create Date: 2022-08-30 02:19:56.932661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a99eda0211c'
down_revision = '42025c22e000'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('settings',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('firstname', sa.String(), nullable=True),
        sa.Column('lastname', sa.String(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('subnet_mask', sa.String(), nullable=True),
        sa.Column('gateway', sa.String(), nullable=True),
        sa.Column('dns', sa.String(), nullable=True),
        sa.Column('longitude', sa.String(), nullable=True),
        sa.Column('latitude', sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('settings')
