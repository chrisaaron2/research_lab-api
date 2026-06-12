from httpx import AsyncClient


async def create_test_publication(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> int:
    response = await async_client.post(
        "/publications",
        headers=auth_headers,
        json={
            "title": "Route Test Publication",
            "venue": "Route Test Venue",
            "date": "2026-04-27",
            "doi": "10.9999/route-test",
        },
    )
    assert response.status_code == 201
    return response.json()["pubid"]


async def test_list_publications(async_client: AsyncClient) -> None:
    response = await async_client.get("/publications")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 25
    assert all("author_count" in publication for publication in data)


async def test_filter_publications_by_year(async_client: AsyncClient) -> None:
    response = await async_client.get("/publications?year=2024")

    assert response.status_code == 200
    data = response.json()
    assert data
    assert all(publication["date"].startswith("2024") for publication in data)


async def test_filter_publications_by_venue(async_client: AsyncClient) -> None:
    all_response = await async_client.get("/publications")
    venue = next(
        publication["venue"]
        for publication in all_response.json()
        if publication["venue"] is not None
    )

    response = await async_client.get("/publications", params={"venue": venue})

    assert response.status_code == 200
    data = response.json()
    assert data
    assert all(publication["venue"] == venue for publication in data)


async def test_filter_publications_by_author(async_client: AsyncClient) -> None:
    response = await async_client.get("/publications?author_mid=1")

    assert response.status_code == 200
    data = response.json()
    assert data

    for publication in data:
        detail_response = await async_client.get(
            f"/publications/{publication['pubid']}"
        )
        authors = detail_response.json()["authors"]
        assert any(author["mid"] == 1 for author in authors)


async def test_get_publication_detail(async_client: AsyncClient) -> None:
    response = await async_client.get("/publications/1")

    assert response.status_code == 200
    data = response.json()
    assert data["pubid"] == 1
    assert "authors" in data
    assert data["authors"]


async def test_get_missing_publication(async_client: AsyncClient) -> None:
    response = await async_client.get("/publications/99999")

    assert response.status_code == 404


async def test_get_publication_authors(async_client: AsyncClient) -> None:
    response = await async_client.get("/publications/1/authors")

    assert response.status_code == 200
    data = response.json()
    assert data
    assert {"mid", "name", "type"}.issubset(data[0])


async def test_create_publication_without_auth_rejected(
    async_client: AsyncClient,
) -> None:
    response = await async_client.post(
        "/publications",
        json={
            "title": "Unauthorized Publication",
            "venue": "Route Test Venue",
            "date": "2026-04-27",
            "doi": "10.9999/unauthorized",
        },
    )

    assert response.status_code == 401


async def test_create_publication_with_auth(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    response = await async_client.post(
        "/publications",
        headers=auth_headers,
        json={
            "title": "Route Test Publication",
            "venue": "Route Test Venue",
            "date": "2026-04-27",
            "doi": "10.9999/route-test-create",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Route Test Publication"
    assert data["authors"] == []


async def test_update_publication_with_auth(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    pubid = await create_test_publication(async_client, auth_headers)

    response = await async_client.put(
        f"/publications/{pubid}",
        headers=auth_headers,
        json={
            "title": "Updated Route Test Publication",
            "venue": "Updated Route Test Venue",
            "date": "2026-05-01",
            "doi": "10.9999/route-test-updated",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Route Test Publication"
    assert data["venue"] == "Updated Route Test Venue"
    assert data["date"] == "2026-05-01"
    assert data["doi"] == "10.9999/route-test-updated"


async def test_delete_publication_with_auth(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    pubid = await create_test_publication(async_client, auth_headers)
    add_response = await async_client.post(
        f"/publications/{pubid}/authors",
        headers=auth_headers,
        json={"mid": 1},
    )
    assert add_response.status_code == 200

    response = await async_client.delete(
        f"/publications/{pubid}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "publication deleted"

    detail_response = await async_client.get(f"/publications/{pubid}")
    assert detail_response.status_code == 404


async def test_add_publication_author_with_auth(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    pubid = await create_test_publication(async_client, auth_headers)

    response = await async_client.post(
        f"/publications/{pubid}/authors",
        headers=auth_headers,
        json={"mid": 1},
    )

    assert response.status_code == 200
    data = response.json()
    assert any(author["mid"] == 1 for author in data["authors"])

    detail_response = await async_client.get(f"/publications/{pubid}")
    detail_authors = detail_response.json()["authors"]
    assert any(author["mid"] == 1 for author in detail_authors)


async def test_add_duplicate_publication_author_rejected(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    pubid = await create_test_publication(async_client, auth_headers)
    first_response = await async_client.post(
        f"/publications/{pubid}/authors",
        headers=auth_headers,
        json={"mid": 1},
    )
    assert first_response.status_code == 200

    response = await async_client.post(
        f"/publications/{pubid}/authors",
        headers=auth_headers,
        json={"mid": 1},
    )

    assert response.status_code == 400
    assert "authorship already exists" in response.json()["detail"]


async def test_add_publication_author_with_invalid_member(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    pubid = await create_test_publication(async_client, auth_headers)

    response = await async_client.post(
        f"/publications/{pubid}/authors",
        headers=auth_headers,
        json={"mid": 99999},
    )

    assert response.status_code == 404
    assert "lab member not found" in response.json()["detail"]


async def test_remove_publication_author_with_auth(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    pubid = await create_test_publication(async_client, auth_headers)
    add_response = await async_client.post(
        f"/publications/{pubid}/authors",
        headers=auth_headers,
        json={"mid": 1},
    )
    assert add_response.status_code == 200

    response = await async_client.delete(
        f"/publications/{pubid}/authors/1",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "authorship deleted"


async def test_remove_missing_publication_author(
    async_client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    pubid = await create_test_publication(async_client, auth_headers)

    response = await async_client.delete(
        f"/publications/{pubid}/authors/1",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert "authorship not found" in response.json()["detail"]
