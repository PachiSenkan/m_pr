"""Init 2

Revision ID: c99d50f07b1b
Revises: 3171b4b1b84d
Create Date: 2024-05-27 10:42:06.131925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c99d50f07b1b'
down_revision: Union[str, None] = '3171b4b1b84d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
