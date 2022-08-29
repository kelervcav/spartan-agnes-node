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
        sa.Column('name', sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('settings')
