"""create olap fk

Revision ID: 2c2420a1ac1b
Revises: 4a0b57fbb9b3
Create Date: 2024-11-26 08:06:41.486834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '2c2420a1ac1b'
down_revision: Union[str, None] = '4a0b57fbb9b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""
    
            ALTER TABLE comradewolf.user_olap DROP CONSTRAINT IF EXISTS user_olap_olap_table_fk;
            ALTER TABLE comradewolf.user_olap ADD CONSTRAINT user_olap_olap_table_fk FOREIGN KEY (id) REFERENCES comradewolf.olap_table(id);


        """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

                ALTER TABLE comradewolf.user_olap DROP CONSTRAINT IF EXISTS user_olap_olap_table_fk;

            """))