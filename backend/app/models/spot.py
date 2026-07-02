import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Float, Boolean, Integer, DateTime, ForeignKey, Text, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from app.db.base import Base


class SpotStatus(str):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class Spot(Base):
    __tablename__ = "spots"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name_ar: Mapped[str] = mapped_column(String(300), nullable=False)
    name_en: Mapped[str | None] = mapped_column(String(300), nullable=True)
    description_ar: Mapped[str] = mapped_column(Text, nullable=False)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    region_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("regions.id"), nullable=False, index=True)
    spot_type: Mapped[str] = mapped_column(
        SAEnum("archaeological", "nature", "waterfall", "desert", "coastal", "village",
               name="spot_type"), nullable=False
    )
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    access_difficulty: Mapped[str] = mapped_column(
        SAEnum("easy", "medium", "hard", name="access_difficulty"), default="medium"
    )
    best_season: Mapped[str | None] = mapped_column(String(100), nullable=True)
    walking_distance_km: Mapped[float | None] = mapped_column(Float, nullable=True)
    visit_duration_hours: Mapped[float | None] = mapped_column(Float, nullable=True)
    requires_4x4: Mapped[bool] = mapped_column(Boolean, default=False)
    has_phone_signal: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[str] = mapped_column(
        SAEnum("pending", "approved", "rejected", name="spot_status"), default="pending", index=True
    )
    submitted_by_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    approved_by_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    ai_quality_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(384), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    region: Mapped["Region"] = relationship("Region", back_populates="spots")
    submitter: Mapped["User | None"] = relationship(
        "User", foreign_keys=[submitted_by_id], back_populates="submitted_spots"
    )
    approver: Mapped["User | None"] = relationship(
        "User", foreign_keys=[approved_by_id], back_populates="approved_spots"
    )
    images: Mapped[list["SpotImage"]] = relationship("SpotImage", back_populates="spot", cascade="all, delete-orphan")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="spot")
    bookings: Mapped[list["Booking"]] = relationship("Booking", back_populates="spot")


class SpotImage(Base):
    __tablename__ = "spot_images"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    spot_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("spots.id", ondelete="CASCADE"), nullable=False, index=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    uploaded_by_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    spot: Mapped["Spot"] = relationship("Spot", back_populates="images")
