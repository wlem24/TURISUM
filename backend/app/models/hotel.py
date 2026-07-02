import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Hotel(Base):
    __tablename__ = "hotels"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name_ar: Mapped[str] = mapped_column(String(300), nullable=False)
    name_en: Mapped[str | None] = mapped_column(String(300), nullable=True)
    region_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("regions.id"), nullable=False, index=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    stars: Mapped[int] = mapped_column(Integer, default=3)
    price_per_night: Mapped[float] = mapped_column(Float, nullable=False)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    commission_rate: Mapped[float] = mapped_column(Float, default=0.10)
    contact_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    website_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    region: Mapped["Region"] = relationship("Region", back_populates="hotels")
    bookings: Mapped[list["Booking"]] = relationship("Booking", foreign_keys="Booking.hotel_id", back_populates="hotel")
