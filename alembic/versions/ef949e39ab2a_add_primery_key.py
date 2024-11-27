"""add primary key

Revision ID: ef949e39ab2a
Revises: 519d79d9dcc9
Create Date: 2024-11-26 20:41:28.180238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'ef949e39ab2a'
down_revision: Union[str, None] = '519d79d9dcc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

            ALTER TABLE comradewolf.forgot_password_code ADD CONSTRAINT forgot_password_code_pk PRIMARY KEY (id);

        """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

                alter table comradewolf.forgot_password_code drop constraint forgot_password_code_pk;

            """))