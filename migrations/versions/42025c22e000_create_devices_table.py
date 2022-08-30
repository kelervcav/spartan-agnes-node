"""create devices table

Revision ID: 42025c22e000
Revises:
Create Date: 2022-08-30 01:40:47.354214

"""
from email.policy import default
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '42025c22e000'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('devices',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('unit', sa.Integer, nullable=False),
        sa.Column('address', sa.Integer, nullable=False),
        sa.Column('status', sa.Boolean, default=False)
    )


def downgrade() -> None:
    op.drop_table('devices')
