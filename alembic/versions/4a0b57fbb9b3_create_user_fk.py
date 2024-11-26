"""create user fk

Revision ID: 4a0b57fbb9b3
Revises: e9651e07444d
Create Date: 2024-11-26 08:00:54.134006

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '4a0b57fbb9b3'
down_revision: Union[str, None] = 'e9651e07444d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""
            ALTER TABLE comradewolf.user_olap DROP CONSTRAINT IF EXISTS user_olap_user_olap_fk;
            ALTER TABLE comradewolf.user_olap ADD CONSTRAINT user_olap_user_olap_fk FOREIGN KEY (user_id) REFERENCES comradewolf.user_olap(id);
        """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

                ALTER TABLE comradewolf.user_olap DROP CONSTRAINT IF EXISTS user_olap_user_olap_fk;

            """))