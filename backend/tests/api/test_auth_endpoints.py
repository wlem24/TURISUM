import pytest
import pytest_asyncio


@pytest.mark.asyncio
async def test_register_success(client):
    response = await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "TestPass123!",
        "full_name": "Test User",
        "role": "visitor",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["role"] == "visitor"
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    payload = {
        "email": "dup@example.com",
        "password": "TestPass123!",
        "full_name": "User",
        "role": "visitor",
    }
    await client.post("/api/v1/auth/register", json=payload)
    response = await client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_admin_role_rejected(client):
    response = await client.post("/api/v1/auth/register", json={
        "email": "admin@evil.com",
        "password": "Test1234!",
        "full_name": "Hacker",
        "role": "admin",
    })
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client):
    await client.post("/api/v1/auth/register", json={
        "email": "login@example.com",
        "password": "LoginPass123!",
        "full_name": "Login User",
        "role": "visitor",
    })
    response = await client.post("/api/v1/auth/login", json={
        "email": "login@example.com",
        "password": "LoginPass123!",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/api/v1/auth/register", json={
        "email": "wrongpass@example.com",
        "password": "Correct123!",
        "full_name": "User",
        "role": "visitor",
    })
    response = await client.post("/api/v1/auth/login", json={
        "email": "wrongpass@example.com",
        "password": "WrongPassword!",
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_me_requires_auth(client):
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_me_with_valid_token(client):
    await client.post("/api/v1/auth/register", json={
        "email": "me@example.com",
        "password": "MePass123!",
        "full_name": "Me User",
        "role": "visitor",
    })
    login = await client.post("/api/v1/auth/login", json={
        "email": "me@example.com",
        "password": "MePass123!",
    })
    token = login.json()["access_token"]

    response = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"
