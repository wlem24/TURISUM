import uuid
from datetime import datetime, timezone
from sqlalchemy import Integer, DateTime, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_reviews_rating"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    spot_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("spots.id"), nullable=True, index=True)
    guide_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("guides.id"), nullable=True, index=True)
    reviewer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment_ar: Mapped[str | None] = mapped_column(Text, nullable=True)
    comment_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    spot: Mapped["Spot | None"] = relationship("Spot", back_populates="reviews")
    guide: Mapped["Guide | None"] = relationship("Guide", back_populates="reviews")
    reviewer: Mapped["User"] = relationship("User", back_populates="reviews")
