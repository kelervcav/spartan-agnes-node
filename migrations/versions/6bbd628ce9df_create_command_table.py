"""Create command table

Revision ID: 6bbd628ce9df
Revises: 41798222ba3f
Create Date: 2022-09-09 16:32:26.374762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6bbd628ce9df'
down_revision = '41798222ba3f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('commands',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('address', sa.String, nullable=False),
        sa.Column('value', sa.String, nullable=False),
        sa.Column('device_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['device_id'], ['devices.id'], )
    )


def downgrade() -> None:
    op.drop_table('commands')
