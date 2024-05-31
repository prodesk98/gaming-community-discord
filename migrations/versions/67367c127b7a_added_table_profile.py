"""added table profile

Revision ID: 67367c127b7a
Revises: 
Create Date: 2024-05-30 05:16:23.234953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67367c127b7a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "profiles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("nick_name", sa.String, nullable=True, default=None),
        sa.Column("guild_id", sa.Integer, nullable=False),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("level", sa.Integer, default=0),
        sa.Column("matches", sa.Integer, default=0),
        sa.Column("wins", sa.Integer, default=0),
        sa.Column("losses", sa.Integer, default=0),
        sa.Column("kills", sa.Integer, default=0),
        sa.Column("assists", sa.Integer, default=0),
        sa.Column("score", sa.Float, default=0.0),
        sa.Column("description", sa.String, default=None, nullable=True),
        sa.Column("avatar", sa.String, default=None, nullable=True),
    )


def downgrade() -> None:
    op.drop_table("profiles")
