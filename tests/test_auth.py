from httpx import AsyncClient


async def test_login_success(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"


async def test_login_invalid_password(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/auth/login",
        json={"username": "admin", "password": "wrong-password"},
    )

    assert response.status_code == 401


async def test_login_unknown_user(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/auth/login",
        json={"username": "unknown", "password": "admin123"},
    )

    assert response.status_code == 401


async def test_public_get_without_token(async_client: AsyncClient) -> None:
    response = await async_client.get("/members/1")

    assert response.status_code == 200


async def test_protected_route_no_token(async_client: AsyncClient) -> None:
    response = await async_client.delete("/members/1")

    assert response.status_code == 401
    assert "missing bearer token" in response.json()["detail"]


async def test_protected_route_viewer_token(
    async_client: AsyncClient,
    viewer_headers: dict[str, str],
) -> None:
    response = await async_client.delete("/members/1", headers=viewer_headers)

    assert response.status_code == 401
    assert "admin privileges" in response.json()["detail"]


async def test_protected_route_admin_token_reaches_business_logic(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    response = await async_client.delete("/members/1", headers=auth_headers)

    assert response.status_code == 400
    assert "dependent records exist" in response.json()["detail"]
