"""added on_delete cascade

Revision ID: f9ab67ac1f5b
Revises: c96a627b2e74
Create Date: 2024-06-04 20:18:01.984071

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'f9ab67ac1f5b'
down_revision: Union[str, None] = 'c96a627b2e74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # likes table: profile_id
    op.drop_constraint('likes_profile_id_fkey', 'likes', type_='foreignkey')
    op.create_foreign_key('likes_profile_id_fkey', 'likes', 'profiles', ['profile_id'], ['id'], ondelete='CASCADE')

    # likes table: target_id
    op.drop_constraint('likes_target_id_fkey', 'likes', type_='foreignkey')
    op.create_foreign_key('likes_target_id_fkey', 'likes', 'profiles', ['target_id'], ['id'], ondelete='CASCADE')

    # weekly table
    op.drop_constraint('weekly_profile_id_fkey', 'weekly', type_='foreignkey')
    op.create_foreign_key('weekly_profile_id_fkey', 'weekly', 'profiles', ['profile_id'], ['id'], ondelete='CASCADE')

    # scores table
    op.drop_constraint('scores_profile_id_fkey', 'scores', type_='foreignkey')
    op.create_foreign_key('scores_profile_id_fkey', 'scores', 'profiles', ['profile_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    pass
