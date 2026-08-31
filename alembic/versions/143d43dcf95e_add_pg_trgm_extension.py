"""add pg trgm extension

Revision ID: 143d43dcf95e
Revises: c6fa0e8c9759
Create Date: 2026-08-28 15:15:57.314366

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '143d43dcf95e'
down_revision: Union[str, Sequence[str], None] = 'c6fa0e8c9759'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")



def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS pg_trgm")