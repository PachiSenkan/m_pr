"""add new tables

Revision ID: 3e893f278f29
Revises: 59aed47590f3
Create Date: 2024-05-27 10:02:53.997767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e893f278f29'
down_revision: Union[str, None] = '59aed47590f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
