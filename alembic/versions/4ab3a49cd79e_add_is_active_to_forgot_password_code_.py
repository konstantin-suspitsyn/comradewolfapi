"""add is_active to forgot_password_code_table

Revision ID: 4ab3a49cd79e
Revises: dfec3e76d5ad
Create Date: 2024-11-27 21:39:55.230710

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '4ab3a49cd79e'
down_revision: Union[str, None] = 'dfec3e76d5ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""
            ALTER TABLE comradewolf.forgot_password_code ADD is_active bool NOT NULL;
        """))


def downgrade() -> None:
    pass