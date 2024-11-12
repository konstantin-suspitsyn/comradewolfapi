"""create cube_info table

Revision ID: feaf9e917515
Revises: 
Create Date: 2024-11-07 21:45:54.834647

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'feaf9e917515'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

            CREATE TABLE IF NOT EXISTS comradewolf.olap_table (
                id bigserial NOT NULL,
                name varchar(50) NOT NULL,
                host varchar(250) NOT NULL,
                port int8 NOT NULL,
                username_env varchar(50) NOT NULL,
                password_env varchar(50) NOT NULL,
                created_at timestamp with time zone NOT NULL,
                updated_at timestamp with time zone NULL,
                CONSTRAINT olap_table_pk PRIMARY KEY (id),
                CONSTRAINT olap_table_name_unique UNIQUE (name),
                CONSTRAINT olap_table_username_unique UNIQUE (username_env),
                CONSTRAINT olap_table_pass_unique UNIQUE (password_env)
            );


        """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

                DROP TABLE comradewolf.olap_table;

            """))
