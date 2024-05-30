"""added likes

Revision ID: b81068fa01ce
Revises: dfee676a2c58
Create Date: 2024-05-30 18:50:15.467776

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b81068fa01ce'
down_revision: Union[str, None] = 'dfee676a2c58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'likes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('profile_id', sa.Integer, sa.ForeignKey('profiles.id'), nullable=False),
        sa.Column('target_id', sa.Integer, sa.ForeignKey('profiles.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('likes')
