"""create olpa_user table

Revision ID: e9651e07444d
Revises: 755bbb2f1a05
Create Date: 2024-11-26 07:58:05.523179

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'e9651e07444d'
down_revision: Union[str, None] = '755bbb2f1a05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

            CREATE TABLE comradewolf.user_olap (
                id bigserial NOT NULL,
                user_id bigint NOT NULL,
                olap_id bigint NOT NULL,
                CONSTRAINT user_olap_pk PRIMARY KEY (id)
            );



        """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

                DROP TABLE comradewolf.user_olap;

            """))