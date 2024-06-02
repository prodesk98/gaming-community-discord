"""added weekly

Revision ID: c96a627b2e74
Revises: 8c30b669e06f
Create Date: 2024-06-02 17:40:40.489488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c96a627b2e74'
down_revision: Union[str, None] = '8c30b669e06f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'weekly',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('profile_id', sa.Integer, sa.ForeignKey('profiles.id')),
        sa.Column('level', sa.Integer),
        sa.Column('kills', sa.Integer),
        sa.Column('wons', sa.Integer),
        sa.Column('losses', sa.Integer),
        sa.Column('assist', sa.Integer),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('weekly')
