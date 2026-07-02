import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app.core.security.permissions import Role


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    full_name_ar: Mapped[str | None] = mapped_column(String(200), nullable=True)
    role: Mapped[str] = mapped_column(
        SAEnum(Role, name="user_role"), default=Role.VISITOR, nullable=False
    )
    region_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("regions.id"), nullable=True
    )
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    region: Mapped["Region | None"] = relationship("Region", back_populates="users")
    submitted_spots: Mapped[list["Spot"]] = relationship(
        "Spot", foreign_keys="Spot.submitted_by_id", back_populates="submitter"
    )
    approved_spots: Mapped[list["Spot"]] = relationship(
        "Spot", foreign_keys="Spot.approved_by_id", back_populates="approver"
    )
    guide_profile: Mapped["Guide | None"] = relationship("Guide", back_populates="user", uselist=False)
    bookings: Mapped[list["Booking"]] = relationship("Booking", foreign_keys="Booking.visitor_id", back_populates="visitor")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="reviewer")
    notifications: Mapped[list["Notification"]] = relationship("Notification", back_populates="user")
    ai_chats: Mapped[list["AIChatHistory"]] = relationship("AIChatHistory", back_populates="user")
