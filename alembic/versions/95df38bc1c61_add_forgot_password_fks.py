"""add forgot_password fks

Revision ID: 95df38bc1c61
Revises: ef949e39ab2a
Create Date: 2024-11-26 20:43:15.176290

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '95df38bc1c61'
down_revision: Union[str, None] = 'ef949e39ab2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""
            ALTER TABLE comradewolf.forgot_password_code DROP CONSTRAINT IF EXISTS forgot_password_code_app_user_fk;
            ALTER TABLE comradewolf.forgot_password_code ADD CONSTRAINT forgot_password_code_app_user_fk FOREIGN KEY (user_id) REFERENCES comradewolf.app_user(id);
        """))


def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(text("""

                ALTER TABLE comradewolf.forgot_password_code DROP CONSTRAINT IF EXISTS forgot_password_code_app_user_fk;

            """))