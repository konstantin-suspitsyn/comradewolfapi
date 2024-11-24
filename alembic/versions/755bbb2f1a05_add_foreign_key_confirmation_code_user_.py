"""add foreign key confirmation_code user_id

Revision ID: 755bbb2f1a05
Revises: aac7f165b992
Create Date: 2024-11-19 22:39:21.822923

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '755bbb2f1a05'
down_revision: Union[str, None] = 'aac7f165b992'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""
            ALTER TABLE comradewolf.confirmation_code DROP CONSTRAINT IF EXISTS confirmation_code_app_user_fk;
            ALTER TABLE comradewolf.confirmation_code ADD CONSTRAINT confirmation_code_app_user_fk FOREIGN KEY (user_id) REFERENCES comradewolf.app_user(id) ON DELETE CASCADE;
        """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

                ALTER TABLE foo DROP CONSTRAINT IF EXISTS comradewolf.confirmation_code;

            """))