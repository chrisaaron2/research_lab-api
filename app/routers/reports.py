from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.reports import (
    get_projects_ended_before,
    get_student_publications_by_major_year,
    get_top_funded_projects,
    get_top_mentors_by_publications,
    get_top_publication_years,
)
from app.db import get_db
from app.schemas.report import (
    ProjectEndedBeforeResponse,
    StudentPublicationByMajorYearResponse,
    TopFundedProjectResponse,
    TopMentorPublicationResponse,
    TopPublicationYearResponse,
)


router = APIRouter(tags=["reports"])


@router.get(
    "/reports/top-funded-projects",
    response_model=list[TopFundedProjectResponse],
)
async def read_top_funded_projects(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[TopFundedProjectResponse]:
    return await get_top_funded_projects(db)


@router.get(
    "/reports/top-mentors-by-publications",
    response_model=list[TopMentorPublicationResponse],
)
async def read_top_mentors_by_publications(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[TopMentorPublicationResponse]:
    return await get_top_mentors_by_publications(db)


@router.get(
    "/reports/student-publications-by-major-year",
    response_model=list[StudentPublicationByMajorYearResponse],
)
async def read_student_publications_by_major_year(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[StudentPublicationByMajorYearResponse]:
    return await get_student_publications_by_major_year(db)


@router.get(
    "/reports/projects-ended-before",
    response_model=list[ProjectEndedBeforeResponse],
)
async def read_projects_ended_before(
    target_date: Annotated[date, Query(alias="date")],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ProjectEndedBeforeResponse]:
    return await get_projects_ended_before(db, target_date)


@router.get(
    "/reports/top-publication-years",
    response_model=list[TopPublicationYearResponse],
)
async def read_top_publication_years(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[TopPublicationYearResponse]:
    return await get_top_publication_years(db)
