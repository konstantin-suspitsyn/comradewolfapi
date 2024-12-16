"""create table confirmation_code

Revision ID: aac7f165b992
Revises: 118964c4b9d5
Create Date: 2024-11-19 22:28:05.139360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'aac7f165b992'
down_revision: Union[str, None] = '118964c4b9d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

            CREATE TABLE IF NOT EXISTS comradewolf.confirmation_code (
                id bigserial NOT NULL,
                code varchar(256) NOT NULL,
                active bool NOT NULL,
                created_at timestamp NOT NULL,
                expires_at timestamp NOT NULL,
                user_id int8 NULL,
                CONSTRAINT confirmation_code_pk PRIMARY KEY (id)
            );


        """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

                DROP TABLE comradewolf.confirmation_code;

            """))