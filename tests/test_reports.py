from datetime import date

from httpx import AsyncClient


async def test_top_funded_projects(async_client: AsyncClient) -> None:
    response = await async_client.get("/reports/top-funded-projects")

    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 5
    assert projects[0]["title"] == "Adaptive Clinical NLP"
    assert "grant_count" in projects[0]
    assert "total_funding" in projects[0]


async def test_top_mentors_by_publications(async_client: AsyncClient) -> None:
    response = await async_client.get("/reports/top-mentors-by-publications")

    assert response.status_code == 200
    mentors = response.json()
    assert mentors
    assert mentors[0]["mentor_name"]
    assert mentors[0]["mentee_pub_count"] > 0


async def test_student_publications_by_major_year(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get("/reports/student-publications-by-major-year")

    assert response.status_code == 200
    rows = response.json()
    assert rows
    for row in rows:
        assert "major" in row
        assert "year" in row
        assert "pub_count" in row


async def test_projects_ended_before(async_client: AsyncClient) -> None:
    response = await async_client.get("/reports/projects-ended-before?date=2024-01-01")

    assert response.status_code == 200
    projects = response.json()
    assert projects
    cutoff = date.fromisoformat("2024-01-01")
    for project in projects:
        assert date.fromisoformat(project["e_date"]) < cutoff


async def test_projects_ended_before_invalid_date(
    async_client: AsyncClient,
) -> None:
    response = await async_client.get("/reports/projects-ended-before?date=not-a-date")

    assert response.status_code == 422


async def test_top_publication_years(async_client: AsyncClient) -> None:
    response = await async_client.get("/reports/top-publication-years")

    assert response.status_code == 200
    years = response.json()
    assert len(years) == 3
    for year in years:
        assert "year" in year
        assert "pub_count" in year
