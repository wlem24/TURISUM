import pytest
from app.schemas.spot import SpotCreate
from pydantic import ValidationError


def test_spot_create_valid():
    spot = SpotCreate(
        name_ar="شلالات عسير",
        description_ar="شلالات طبيعية رائعة في منطقة عسير",
        region_id="00000000-0000-0000-0000-000000000001",
        spot_type="waterfall",
        latitude=18.5,
        longitude=42.5,
    )
    assert spot.name_ar == "شلالات عسير"
    assert spot.spot_type == "waterfall"
    assert spot.access_difficulty == "medium"


def test_spot_latitude_outside_saudi_rejected():
    with pytest.raises(ValidationError) as exc_info:
        SpotCreate(
            name_ar="موقع خارج المملكة",
            description_ar="وصف",
            region_id="00000000-0000-0000-0000-000000000001",
            spot_type="nature",
            latitude=51.5,  # London
            longitude=46.0,
        )
    assert "Latitude" in str(exc_info.value)


def test_spot_longitude_outside_saudi_rejected():
    with pytest.raises(ValidationError):
        SpotCreate(
            name_ar="موقع",
            description_ar="وصف",
            region_id="00000000-0000-0000-0000-000000000001",
            spot_type="nature",
            latitude=24.0,
            longitude=70.0,  # Outside Saudi
        )


def test_spot_valid_boundary():
    spot = SpotCreate(
        name_ar="موقع حدودي",
        description_ar="وصف",
        region_id="00000000-0000-0000-0000-000000000001",
        spot_type="desert",
        latitude=16.0,
        longitude=34.5,
    )
    assert spot.latitude == 16.0
