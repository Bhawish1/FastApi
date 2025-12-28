"""rename Phone_number to phone_number

Revision ID: 13c1ebd1bb32
Revises: 829ed9d8c462
Create Date: 2025-12-25 19:45:40.127815

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13c1ebd1bb32'
down_revision: Union[str, Sequence[str], None] = '829ed9d8c462'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "users",
        "Phone_number",
        new_column_name="phone_number"
        )


def downgrade() -> None:
    """Downgrade schema."""
    pass
