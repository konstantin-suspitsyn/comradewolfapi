"""create app_user table

Revision ID: a1048ca7eb34
Revises: feaf9e917515
Create Date: 2024-11-09 18:35:55.130239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'a1048ca7eb34'
down_revision: Union[str, None] = 'feaf9e917515'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

            CREATE TABLE IF NOT EXISTS comradewolf.app_user (
                id bigserial NOT NULL,
                username varchar(50) NOT NULL,
                "password" varchar(256) NOT NULL,
                email varchar(250) NOT NULL,
                is_active bool NOT NULL,
                created_at timestamp NOT NULL,
                updated_at timestamp NULL,
                CONSTRAINT app_user_pk PRIMARY KEY (id),
                CONSTRAINT app_user_username UNIQUE (username),
                CONSTRAINT app_user_email UNIQUE (email)
            );


        """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

                DROP TABLE comradewolf.app_user;

            """))