from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True, default=uuid4)
    scan_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True),
        ForeignKey("menu_scans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    position: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    name_original: Mapped[str] = mapped_column(String(300), nullable=False)
    name_translated: Mapped[str | None] = mapped_column(String(300))
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(String(100))
    price: Mapped[float | None] = mapped_column(Numeric(10, 2))
    currency: Mapped[str | None] = mapped_column(String(10))
    ingredients: Mapped[list[str] | None] = mapped_column(JSON)
    allergens: Mapped[list[str] | None] = mapped_column(JSON)
    is_vegetarian: Mapped[bool | None] = mapped_column()
    is_vegan: Mapped[bool | None] = mapped_column()
    is_halal_possible: Mapped[bool | None] = mapped_column()
    spice_level: Mapped[int | None] = mapped_column(Integer)

    allergen_risk: Mapped[str | None] = mapped_column(String(10))
    hidden_risks: Mapped[list[str] | None] = mapped_column(JSON)
    local_popularity: Mapped[str | None] = mapped_column(String(10))
    tourist_trap_risk: Mapped[str | None] = mapped_column(String(10))
    value_assessment: Mapped[str | None] = mapped_column(String(15))
    recommendation_score: Mapped[int | None] = mapped_column(Integer)
    cultural_context: Mapped[dict | None] = mapped_column(JSON)
    ai_metadata: Mapped[dict | None] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    scan: Mapped["MenuScan"] = relationship(back_populates="dishes")  # noqa: F821
    favorites: Mapped[list["Favorite"]] = relationship(  # noqa: F821
        back_populates="dish", cascade="all, delete-orphan"
    )
