"""change olap_user pk fk

Revision ID: dfec3e76d5ad
Revises: 95df38bc1c61
Create Date: 2024-11-26 21:21:28.638289

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'dfec3e76d5ad'
down_revision: Union[str, None] = '95df38bc1c61'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""
            ALTER TABLE comradewolf.user_olap DROP CONSTRAINT user_olap_pk cascade;
            ALTER TABLE comradewolf.user_olap DROP CONSTRAINT user_olap_olap_table_fk cascade;
            ALTER TABLE comradewolf.user_olap DROP COLUMN id;
            ALTER TABLE comradewolf.user_olap ADD CONSTRAINT user_olap_pk PRIMARY KEY (user_id,olap_id);
            ALTER TABLE comradewolf.user_olap ADD CONSTRAINT user_olap_olap_table_fk FOREIGN KEY (olap_id) REFERENCES comradewolf.olap_table(id);

        """))


def downgrade() -> None:
    pass