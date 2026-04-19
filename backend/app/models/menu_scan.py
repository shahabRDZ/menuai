from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import JSON, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MenuScan(Base):
    __tablename__ = "menu_scans"

    id: Mapped[UUID] = mapped_column(PgUUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(
        PgUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    image_url: Mapped[str | None] = mapped_column(String(500))
    restaurant_name: Mapped[str | None] = mapped_column(String(200))
    location: Mapped[str | None] = mapped_column(String(200))
    cuisine_type: Mapped[str | None] = mapped_column(String(100))
    source_language: Mapped[str] = mapped_column(String(10), default="auto", nullable=False)
    target_language: Mapped[str] = mapped_column(String(10), default="en", nullable=False)

    ai_recommendations: Mapped[dict | None] = mapped_column(JSON)
    order_suggestions: Mapped[dict | None] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="menu_scans")  # noqa: F821
    dishes: Mapped[list["Dish"]] = relationship(  # noqa: F821
        back_populates="scan", cascade="all, delete-orphan", order_by="Dish.position"
    )
