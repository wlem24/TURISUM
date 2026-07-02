from app.tasks.celery_app import celery_app
from app.core.config import settings


@celery_app.task(name="send_booking_confirmation_email")
def send_booking_confirmation_email(to_email: str, booking_id: str, user_name: str):
    """Send booking confirmation email (stub — wire up SMTP in production)."""
    # In production: use aiosmtplib or SendGrid/SES
    print(f"[EMAIL] Booking confirmation to {to_email}: booking {booking_id} for {user_name}")


@celery_app.task(name="send_spot_approval_email")
def send_spot_approval_email(to_email: str, spot_name: str, approved: bool, reason: str = ""):
    status = "approved" if approved else "rejected"
    print(f"[EMAIL] Spot '{spot_name}' {status} → {to_email}. Reason: {reason}")
