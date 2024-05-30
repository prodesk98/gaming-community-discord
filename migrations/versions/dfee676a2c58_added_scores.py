"""added scores

Revision ID: dfee676a2c58
Revises: 67367c127b7a
Create Date: 2024-05-30 17:51:57.992275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dfee676a2c58'
down_revision: Union[str, None] = '67367c127b7a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'scores',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('profile_id', sa.Integer, sa.ForeignKey('profiles.id')),
        sa.Column('value', sa.Integer, default=0),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('scores')
