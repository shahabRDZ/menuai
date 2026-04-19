"""price intelligence on dishes

Revision ID: 0003_price_intelligence
Revises: 0002_enriched_ai_metadata
Create Date: 2026-04-19
"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

revision: str = "0003_price_intelligence"
down_revision: Union[str, None] = "0002_enriched_ai_metadata"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("dishes", sa.Column("price_usd", sa.Numeric(10, 2)))
    op.add_column("dishes", sa.Column("typical_price_min", sa.Numeric(10, 2)))
    op.add_column("dishes", sa.Column("typical_price_max", sa.Numeric(10, 2)))
    op.add_column("dishes", sa.Column("price_fairness", sa.String(20)))
    op.add_column("dishes", sa.Column("price_delta_percent", sa.Integer))
    op.add_column("dishes", sa.Column("price_estimate_confidence", sa.String(10)))


def downgrade() -> None:
    for col in (
        "price_estimate_confidence",
        "price_delta_percent",
        "price_fairness",
        "typical_price_max",
        "typical_price_min",
        "price_usd",
    ):
        op.drop_column("dishes", col)
