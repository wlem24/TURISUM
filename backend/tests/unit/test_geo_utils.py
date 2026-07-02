import pytest
from app.utils.geo import haversine_km, is_within_saudi_arabia, bounding_box


def test_haversine_riyadh_jeddah():
    # Riyadh to Jeddah ≈ 950 km
    dist = haversine_km(24.7136, 46.6753, 21.4858, 39.1925)
    assert 900 <= dist <= 1000


def test_haversine_same_point():
    assert haversine_km(24.0, 46.0, 24.0, 46.0) == pytest.approx(0.0, abs=0.01)


def test_is_within_saudi_arabia_riyadh():
    assert is_within_saudi_arabia(24.7136, 46.6753) is True


def test_is_within_saudi_arabia_outside():
    assert is_within_saudi_arabia(51.5074, -0.1278) is False  # London


def test_is_within_saudi_boundary_edge():
    assert is_within_saudi_arabia(16.0, 34.5) is True
    assert is_within_saudi_arabia(32.5, 56.0) is True
    assert is_within_saudi_arabia(15.9, 34.5) is False


def test_bounding_box():
    min_lat, max_lat, min_lng, max_lng = bounding_box(24.0, 46.0, 100)
    assert min_lat < 24.0 < max_lat
    assert min_lng < 46.0 < max_lng
