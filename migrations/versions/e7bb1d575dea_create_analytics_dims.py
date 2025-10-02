"""create analytics dims

Revision ID: e7bb1d575dea
Revises: d2e4dd7711c5
Create Date: 2025-09-30 23:32:59.192506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pathlib


# revision identifiers, used by Alembic.
revision: str = 'e7bb1d575dea'
down_revision: Union[str, Sequence[str], None] = 'd2e4dd7711c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    sql_dir = pathlib.Path(__file__).parents[2] / "sql"
    for sql_file in sorted(sql_dir.glob("*dim_*.sql")):
        with open(sql_file, 'r') as file:
            op.execute(file.read())


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE IF EXISTS dim_admission_source CASCADE;")
    op.execute("DROP TABLE IF EXISTS dim_admission_type CASCADE;")
    op.execute("DROP TABLE IF EXISTS dim_medical_specialty CASCADE;")
    op.execute("DROP TABLE IF EXISTS dim_discharge_disposition CASCADE;")
    op.execute("DROP TABLE IF EXISTS dim_diagnosis CASCADE;")
    op.execute("DROP TABLE IF EXISTS dim_payer CASCADE;")
    op.execute("DROP TABLE IF EXISTS dim_patient CASCADE;")
    op.execute("DROP TABLE IF EXISTS dim_treatment CASCADE;")
    op.execute("DROP SCHEMA IF EXISTS analytics CASCADE;")
