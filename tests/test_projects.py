from httpx import AsyncClient


async def test_list_projects(async_client: AsyncClient) -> None:
    response = await async_client.get("/projects")

    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 8
    assert any(project["title"] == "Adaptive Clinical NLP" for project in projects)


async def test_filter_active_projects(async_client: AsyncClient) -> None:
    response = await async_client.get("/projects?status=active")

    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 4
    assert all(project["e_date"] is not None for project in projects)


async def test_filter_completed_projects(async_client: AsyncClient) -> None:
    response = await async_client.get("/projects?status=completed")

    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 4


async def test_get_project_detail(async_client: AsyncClient) -> None:
    response = await async_client.get("/projects/1")

    assert response.status_code == 200
    project = response.json()
    assert project["title"] == "Adaptive Clinical NLP"
    assert project["member_count"] == 4
    assert project["grant_count"] == 2
    assert project["total_funding"]


async def test_project_status(async_client: AsyncClient) -> None:
    response = await async_client.get("/projects/1/status")

    assert response.status_code == 200
    project_status = response.json()
    assert project_status["status"] == "Active"
    assert isinstance(project_status["days_remaining"], int)
    assert project_status["days_remaining"] > 0


async def test_create_update_delete_project_with_auth(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    create_response = await async_client.post(
        "/projects",
        headers=auth_headers,
        json={
            "title": "Route Test Project",
            "s_date": "2026-04-27",
            "e_date": "2028-04-27",
            "e_duration": "24 months",
            "leader": 7,
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    pid = created["pid"]

    update_response = await async_client.put(
        f"/projects/{pid}",
        headers=auth_headers,
        json={"title": "Route Test Project Updated", "leader": 8},
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["leader"] == 8
    assert updated["leader_name"] == "Dr. Benjamin Lee"

    delete_response = await async_client.delete(
        f"/projects/{pid}",
        headers=auth_headers,
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "project deleted"


async def test_delete_seeded_project_blocked(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    response = await async_client.delete("/projects/1", headers=auth_headers)

    assert response.status_code == 400
    assert "dependent records exist" in response.json()["detail"]
