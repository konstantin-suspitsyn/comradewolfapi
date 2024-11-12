"""alter saved_query add pages and items per page

Revision ID: 118964c4b9d5
Revises: fd44216cc86a
Create Date: 2024-11-10 21:51:03.831771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '118964c4b9d5'
down_revision: Union[str, None] = 'fd44216cc86a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

        ALTER TABLE comradewolf.saved_query ADD pages int4 NOT NULL;
        ALTER TABLE comradewolf.saved_query ADD items_per_page int4 NULL;

        """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

            ALTER TABLE comradewolf.saved_query DROP COLUMN pages;
            ALTER TABLE comradewolf.saved_query DROP COLUMN items_per_page;

            """))