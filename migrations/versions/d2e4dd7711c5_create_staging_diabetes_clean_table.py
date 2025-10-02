"""create staging.diabetes_clean table

Revision ID: d2e4dd7711c5
Revises: 
Create Date: 2025-09-28 17:06:36.694889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pathlib


# revision identifiers, used by Alembic.
revision: str = 'd2e4dd7711c5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    sql_file = pathlib.Path(__file__).parents[2] / "sql" / "staging_diabetes.sql"
    with open(sql_file, 'r') as file:
        op.execute(file.read())


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE IF EXISTS staging.diabetes_clean CASCADE;")
    op.execute("DROP SCHEMA IF EXISTS staging CASCADE;")
