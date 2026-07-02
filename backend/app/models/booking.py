import uuid
from datetime import datetime, date, timezone
from decimal import Decimal
from sqlalchemy import String, DateTime, Date, ForeignKey, Text, Numeric, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    booking_type: Mapped[str] = mapped_column(
        SAEnum("guide", "hotel", "package", name="booking_type"), nullable=False
    )
    visitor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    guide_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("guides.id"), nullable=True, index=True)
    hotel_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("hotels.id"), nullable=True, index=True)
    spot_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("spots.id"), nullable=True, index=True)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    commission_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    provider_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    status: Mapped[str] = mapped_column(
        SAEnum("pending", "confirmed", "completed", "cancelled", name="booking_status"),
        default="pending", index=True
    )
    booking_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    payment_reference: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    visitor: Mapped["User"] = relationship("User", foreign_keys=[visitor_id], back_populates="bookings")
    guide: Mapped["Guide | None"] = relationship("Guide", foreign_keys=[guide_id], back_populates="bookings")
    hotel: Mapped["Hotel | None"] = relationship("Hotel", foreign_keys=[hotel_id], back_populates="bookings")
    spot: Mapped["Spot | None"] = relationship("Spot", back_populates="bookings")
