import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, Boolean, Integer, DateTime, ForeignKey, Text, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Guide(Base):
    __tablename__ = "guides"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    bio_ar: Mapped[str | None] = mapped_column(Text, nullable=True)
    bio_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    region_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("regions.id"), nullable=False, index=True)
    specializations: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    languages: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    daily_rate: Mapped[float] = mapped_column(Float, default=0.0)
    rating: Mapped[float] = mapped_column(Float, default=0.0)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    years_experience: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    user: Mapped["User"] = relationship("User", back_populates="guide_profile")
    region: Mapped["Region"] = relationship("Region", back_populates="guides")
    bookings: Mapped[list["Booking"]] = relationship("Booking", foreign_keys="Booking.guide_id", back_populates="guide")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="guide")
