"""create forgot_password_code table

Revision ID: 519d79d9dcc9
Revises: 2c2420a1ac1b
Create Date: 2024-11-26 08:59:10.936969

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '519d79d9dcc9'
down_revision: Union[str, None] = '2c2420a1ac1b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

            CREATE TABLE comradewolf.forgot_password_code (
                id bigserial NOT NULL,
                user_id bigint NOT NULL,
                code varchar(256) NOT NULL,
                created_at timestamp NOT NULL,
                expires_at timestamp NOT NULL,
                updated_at timestamp NOT NULL
            );

        """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

                DROP TABLE comradewolf.forgot_password_code;

            """))