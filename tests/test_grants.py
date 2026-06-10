from httpx import AsyncClient


async def test_list_grants(async_client: AsyncClient) -> None:
    response = await async_client.get("/grants")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    assert any(grant["agency"] == "NSF" for grant in data)


async def test_filter_grants_by_project(async_client: AsyncClient) -> None:
    response = await async_client.get("/grants?pid=1")

    assert response.status_code == 200
    data = response.json()
    assert data
    assert all(grant["pid"] == 1 for grant in data)


async def test_get_grant_detail(async_client: AsyncClient) -> None:
    response = await async_client.get("/grants/1")

    assert response.status_code == 200
    data = response.json()
    assert data["gid"] == 1
    assert data["project_title"] == "Adaptive Clinical NLP"


async def test_get_missing_grant(async_client: AsyncClient) -> None:
    response = await async_client.get("/grants/99999")

    assert response.status_code == 404


async def test_create_grant_without_auth_rejected(async_client: AsyncClient) -> None:
    response = await async_client.post(
        "/grants",
        json={
            "p_duration": "12 months",
            "agency": "Route Test Agency",
            "budget": "75000",
            "start_date": "2026-04-27",
            "pid": 1,
        },
    )

    assert response.status_code == 401


async def test_create_grant_with_auth(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    response = await async_client.post(
        "/grants",
        headers=auth_headers,
        json={
            "p_duration": "12 months",
            "agency": "Route Test Agency",
            "budget": "75000",
            "start_date": "2026-04-27",
            "pid": 1,
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["agency"] == "Route Test Agency"
    assert data["pid"] == 1
    assert data["project_title"] == "Adaptive Clinical NLP"


async def test_create_grant_with_invalid_project(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    response = await async_client.post(
        "/grants",
        headers=auth_headers,
        json={
            "p_duration": "12 months",
            "agency": "Invalid Project Agency",
            "budget": "75000",
            "start_date": "2026-04-27",
            "pid": 99999,
        },
    )

    assert response.status_code == 400
    assert "project not found" in response.json()["detail"]


async def test_update_grant_with_auth(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    create_response = await async_client.post(
        "/grants",
        headers=auth_headers,
        json={
            "p_duration": "18 months",
            "agency": "Before Update Agency",
            "budget": "90000",
            "start_date": "2026-04-27",
            "pid": 1,
        },
    )
    gid = create_response.json()["gid"]

    response = await async_client.put(
        f"/grants/{gid}",
        headers=auth_headers,
        json={
            "agency": "Updated Route Test Agency",
            "budget": "125000",
            "pid": 2,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["agency"] == "Updated Route Test Agency"
    assert data["budget"] == "125000"
    assert data["pid"] == 2
    assert data["project_title"] == "Robotic Lab Automation"


async def test_update_grant_with_invalid_project(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    response = await async_client.put(
        "/grants/1",
        headers=auth_headers,
        json={"pid": 99999},
    )

    assert response.status_code == 400
    assert "project not found" in response.json()["detail"]


async def test_delete_grant_with_auth(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    create_response = await async_client.post(
        "/grants",
        headers=auth_headers,
        json={
            "p_duration": "6 months",
            "agency": "Delete Route Test Agency",
            "budget": "50000",
            "start_date": "2026-04-27",
            "pid": 1,
        },
    )
    gid = create_response.json()["gid"]

    response = await async_client.delete(f"/grants/{gid}", headers=auth_headers)

    assert response.status_code == 200
    assert response.json()["message"] == "grant deleted"


async def test_delete_missing_grant(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    response = await async_client.delete("/grants/99999", headers=auth_headers)

    assert response.status_code == 404
