import pytest
from decimal import Decimal


def calculate_guide_booking(daily_rate: float) -> dict:
    total = Decimal(str(daily_rate))
    commission = (total * Decimal("0.20")).quantize(Decimal("0.01"))
    provider = (total - commission).quantize(Decimal("0.01"))
    return {"total": total, "commission": commission, "provider": provider}


def calculate_hotel_booking(price_per_night: float, commission_rate: float = 0.10) -> dict:
    total = Decimal(str(price_per_night))
    commission = (total * Decimal(str(commission_rate))).quantize(Decimal("0.01"))
    provider = (total - commission).quantize(Decimal("0.01"))
    return {"total": total, "commission": commission, "provider": provider}


@pytest.mark.asyncio
async def test_guide_booking_commission_calculation():
    result = calculate_guide_booking(800.0)
    assert result["total"] == Decimal("800.00")
    assert result["commission"] == Decimal("160.00")
    assert result["provider"] == Decimal("640.00")
    assert result["total"] == result["commission"] + result["provider"]


@pytest.mark.asyncio
async def test_hotel_booking_commission_calculation():
    result = calculate_hotel_booking(600.0, 0.10)
    assert result["total"] == Decimal("600.00")
    assert result["commission"] == Decimal("60.00")
    assert result["provider"] == Decimal("540.00")


@pytest.mark.asyncio
async def test_package_booking_blended_commission():
    guide = calculate_guide_booking(1000.0)
    hotel = calculate_hotel_booking(700.0, 0.10)
    total = guide["total"] + hotel["total"]
    commission = guide["commission"] + hotel["commission"]
    provider = guide["provider"] + hotel["provider"]
    assert total == Decimal("1700.00")
    assert commission == Decimal("270.00")
    assert provider == Decimal("1430.00")
    assert total == commission + provider
