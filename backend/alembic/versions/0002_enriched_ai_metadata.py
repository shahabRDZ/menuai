"""enriched ai metadata on dishes and scans

Revision ID: 0002_enriched_ai_metadata
Revises: 0001_initial
Create Date: 2026-04-19
"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

revision: str = "0002_enriched_ai_metadata"
down_revision: Union[str, None] = "0001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("menu_scans", sa.Column("location", sa.String(200)))
    op.add_column("menu_scans", sa.Column("cuisine_type", sa.String(100)))
    op.add_column("menu_scans", sa.Column("ai_recommendations", sa.JSON))
    op.add_column("menu_scans", sa.Column("order_suggestions", sa.JSON))

    op.add_column("dishes", sa.Column("is_halal_possible", sa.Boolean))
    op.add_column("dishes", sa.Column("allergen_risk", sa.String(10)))
    op.add_column("dishes", sa.Column("hidden_risks", sa.JSON))
    op.add_column("dishes", sa.Column("local_popularity", sa.String(10)))
    op.add_column("dishes", sa.Column("tourist_trap_risk", sa.String(10)))
    op.add_column("dishes", sa.Column("value_assessment", sa.String(15)))
    op.add_column("dishes", sa.Column("recommendation_score", sa.Integer))
    op.add_column("dishes", sa.Column("cultural_context", sa.JSON))
    op.add_column("dishes", sa.Column("ai_metadata", sa.JSON))


def downgrade() -> None:
    for col in (
        "ai_metadata",
        "cultural_context",
        "recommendation_score",
        "value_assessment",
        "tourist_trap_risk",
        "local_popularity",
        "hidden_risks",
        "allergen_risk",
        "is_halal_possible",
    ):
        op.drop_column("dishes", col)

    for col in ("order_suggestions", "ai_recommendations", "cuisine_type", "location"):
        op.drop_column("menu_scans", col)
