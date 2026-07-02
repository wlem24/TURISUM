import pytest


async def _create_user_and_login(client, email: str, role: str = "local") -> str:
    await client.post("/api/v1/auth/register", json={
        "email": email,
        "password": "TestPass123!",
        "full_name": "Test User",
        "role": role,
    })
    resp = await client.post("/api/v1/auth/login", json={
        "email": email,
        "password": "TestPass123!",
    })
    return resp.json()["access_token"]


@pytest.mark.asyncio
async def test_list_spots_public(client):
    response = await client.get("/api/v1/spots")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data


@pytest.mark.asyncio
async def test_submit_spot_requires_local_role(client):
    token = await _create_user_and_login(client, "visitor_spot@example.com", "visitor")
    response = await client.post(
        "/api/v1/spots",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name_ar": "موقع جميل",
            "description_ar": "مكان رائع",
            "region_id": "00000000-0000-0000-0000-000000000001",
            "spot_type": "nature",
            "latitude": 24.0,
            "longitude": 46.0,
        },
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_submit_spot_as_local(client):
    token = await _create_user_and_login(client, "local_spot@example.com", "local")
    response = await client.post(
        "/api/v1/spots",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name_ar": "شلال عسير",
            "description_ar": "شلال طبيعي جميل في منطقة عسير",
            "region_id": "00000000-0000-0000-0000-000000000001",
            "spot_type": "waterfall",
            "latitude": 18.5,
            "longitude": 42.5,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert data["name_ar"] == "شلال عسير"


@pytest.mark.asyncio
async def test_spot_coordinate_validation(client):
    token = await _create_user_and_login(client, "local_coord@example.com", "local")
    response = await client.post(
        "/api/v1/spots",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name_ar": "موقع خارج المملكة",
            "description_ar": "وصف",
            "region_id": "00000000-0000-0000-0000-000000000001",
            "spot_type": "nature",
            "latitude": 51.5,  # London
            "longitude": 46.0,
        },
    )
    assert response.status_code == 422
