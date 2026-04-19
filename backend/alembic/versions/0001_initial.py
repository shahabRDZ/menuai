"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-04-19
"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("name", sa.String(100)),
        sa.Column("native_language", sa.String(10), nullable=False, server_default="en"),
        sa.Column("target_language", sa.String(10), nullable=False, server_default="en"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "menu_scans",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("image_url", sa.String(500)),
        sa.Column("restaurant_name", sa.String(200)),
        sa.Column("source_language", sa.String(10), nullable=False, server_default="auto"),
        sa.Column("target_language", sa.String(10), nullable=False, server_default="en"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index("ix_menu_scans_user_id", "menu_scans", ["user_id"])

    op.create_table(
        "dishes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "scan_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("menu_scans.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("position", sa.Integer, nullable=False, server_default="0"),
        sa.Column("name_original", sa.String(300), nullable=False),
        sa.Column("name_translated", sa.String(300)),
        sa.Column("description", sa.Text),
        sa.Column("category", sa.String(100)),
        sa.Column("price", sa.Numeric(10, 2)),
        sa.Column("currency", sa.String(10)),
        sa.Column("ingredients", sa.JSON),
        sa.Column("allergens", sa.JSON),
        sa.Column("is_vegetarian", sa.Boolean),
        sa.Column("is_vegan", sa.Boolean),
        sa.Column("spice_level", sa.Integer),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )
    op.create_index("ix_dishes_scan_id", "dishes", ["scan_id"])

    op.create_table(
        "favorites",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "dish_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("dishes.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.UniqueConstraint("user_id", "dish_id", name="uq_user_dish"),
    )
    op.create_index("ix_favorites_user_id", "favorites", ["user_id"])
    op.create_index("ix_favorites_dish_id", "favorites", ["dish_id"])


def downgrade() -> None:
    op.drop_table("favorites")
    op.drop_table("dishes")
    op.drop_table("menu_scans")
    op.drop_table("users")
