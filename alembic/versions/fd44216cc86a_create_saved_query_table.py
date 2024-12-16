"""create saved_query table

Revision ID: fd44216cc86a
Revises: a1048ca7eb34
Create Date: 2024-11-09 18:37:36.690798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'fd44216cc86a'
down_revision: Union[str, None] = 'a1048ca7eb34'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

            CREATE TABLE IF NOT EXISTS comradewolf.saved_query (
                id bigserial NOT NULL,
                frontend varchar NOT NULL,
                query varchar NOT NULL,
                CONSTRAINT saved_query_pk PRIMARY KEY (id)
            );
            
        """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

                DROP TABLE comradewolf.saved_query;

            """))