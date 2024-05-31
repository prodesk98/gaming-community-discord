"""added updated at and last stats

Revision ID: 8c30b669e06f
Revises: b81068fa01ce
Create Date: 2024-05-31 15:53:04.181839

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c30b669e06f'
down_revision: Union[str, None] = 'b81068fa01ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'profiles',
        sa.Column('last_stats', sa.JSON, default={})
    )
    op.add_column(
        'profiles',
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
    )


def downgrade() -> None:
    op.drop_column('profiles', 'updated_at')
    op.drop_column('profiles', 'last_stats')
