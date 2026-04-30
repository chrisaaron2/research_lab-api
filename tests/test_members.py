from httpx import AsyncClient


async def test_list_members(async_client: AsyncClient) -> None:
    response = await async_client.get("/members")

    assert response.status_code == 200
    members = response.json()
    assert len(members) == 18
    assert any(member["name"] == "Maya Chen" for member in members)


async def test_filter_student_members(async_client: AsyncClient) -> None:
    response = await async_client.get("/members?type=student")

    assert response.status_code == 200
    members = response.json()
    assert len(members) == 6
    assert all(member["type"] == "student" for member in members)


async def test_get_member_detail(async_client: AsyncClient) -> None:
    response = await async_client.get("/members/1")

    assert response.status_code == 200
    member = response.json()
    assert member["name"] == "Maya Chen"
    assert member["type"] == "student"
    assert member["sid"] == "S1001"


async def test_get_missing_member(async_client: AsyncClient) -> None:
    response = await async_client.get("/members/99999")

    assert response.status_code == 404


async def test_create_update_delete_member_with_auth(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    create_response = await async_client.post(
        "/members",
        headers=auth_headers,
        json={
            "name": "Route Test Student",
            "type": "student",
            "sid": "S7777",
            "level": "MS",
            "major": "Data Science",
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    mid = created["mid"]

    update_response = await async_client.put(
        f"/members/{mid}",
        headers=auth_headers,
        json={"mentor": 7, "major": "Computer Science"},
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["mentor"] == 7
    assert updated["major"] == "Computer Science"

    delete_response = await async_client.delete(
        f"/members/{mid}",
        headers=auth_headers,
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "member deleted"


async def test_create_member_without_auth_rejected(
    async_client: AsyncClient,
) -> None:
    response = await async_client.post(
        "/members",
        json={
            "name": "No Auth Student",
            "type": "student",
            "sid": "S8888",
        },
    )

    assert response.status_code == 401


async def test_grant_members_report_endpoint(async_client: AsyncClient) -> None:
    response = await async_client.get("/grants/1/members")

    assert response.status_code == 200
    members = response.json()
    assert members
    assert any(member["name"] == "Maya Chen" for member in members)


async def test_project_mentorships_endpoint(async_client: AsyncClient) -> None:
    response = await async_client.get("/projects/7/mentorships")

    assert response.status_code == 200
    mentorships = response.json()
    assert mentorships
    first = mentorships[0]
    assert "mentor_mid" in first
    assert "mentor_name" in first
    assert "mentee_mid" in first
    assert "mentee_name" in first
