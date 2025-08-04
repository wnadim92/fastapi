"""add content column to posts table

Revision ID: 14e6828b79f0
Revises: b6e90b7e72c4
Create Date: 2025-08-03 22:35:40.829070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14e6828b79f0'
down_revision: Union[str, Sequence[str], None] = 'b6e90b7e72c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
