"""create analytics fact

Revision ID: 9e371fb7325c
Revises: e7bb1d575dea
Create Date: 2025-09-30 23:40:22.773971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pathlib


# revision identifiers, used by Alembic.
revision: str = '9e371fb7325c'
down_revision: Union[str, Sequence[str], None] = 'e7bb1d575dea'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    sql_file = pathlib.Path(__file__).parents[2] / "sql" / "fact_admission.sql"
    with open(sql_file, 'r') as file:
        op.execute(file.read())


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE IF EXISTS fact_admission CASCADE;")
    op.execute("DROP SCHEMA IF EXISTS analytics CASCADE;")
