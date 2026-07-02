import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Region(Base):
    __tablename__ = "regions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name_ar: Mapped[str] = mapped_column(String(100), nullable=False)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    spot_count: Mapped[int] = mapped_column(Integer, default=0)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    spots: Mapped[list["Spot"]] = relationship("Spot", back_populates="region")
    users: Mapped[list["User"]] = relationship("User", back_populates="region")
    guides: Mapped[list["Guide"]] = relationship("Guide", back_populates="region")
    hotels: Mapped[list["Hotel"]] = relationship("Hotel", back_populates="region")
