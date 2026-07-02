from decimal import Decimal
import pytest


def calculate_amounts(rate: float, commission_pct: float) -> tuple[Decimal, Decimal, Decimal]:
    total = Decimal(str(rate))
    commission = (total * Decimal(str(commission_pct))).quantize(Decimal("0.01"))
    provider = (total - commission).quantize(Decimal("0.01"))
    return total, commission, provider


def test_guide_commission_20_percent():
    total, commission, provider = calculate_amounts(1000.0, 0.20)
    assert total == Decimal("1000.00")
    assert commission == Decimal("200.00")
    assert provider == Decimal("800.00")
    assert total == commission + provider


def test_hotel_commission_10_percent():
    total, commission, provider = calculate_amounts(500.0, 0.10)
    assert total == Decimal("500.00")
    assert commission == Decimal("50.00")
    assert provider == Decimal("450.00")


def test_commission_precision():
    total, commission, provider = calculate_amounts(333.33, 0.20)
    assert commission == Decimal("66.67")
    assert provider == Decimal("266.66")
    # Allow 1 cent rounding difference
    assert abs(total - commission - provider) <= Decimal("0.01")


def test_zero_commission():
    total, commission, provider = calculate_amounts(0.0, 0.20)
    assert total == Decimal("0.00")
    assert commission == Decimal("0.00")
    assert provider == Decimal("0.00")
