"""New

Revision ID: 3171b4b1b84d
Revises: 3e893f278f29
Create Date: 2024-05-27 10:14:19.963816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3171b4b1b84d'
down_revision: Union[str, None] = '3e893f278f29'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
