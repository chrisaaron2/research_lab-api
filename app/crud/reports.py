from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.models import Grant, LabMember, Project, Publication, Publishes, Student
from app.schemas.report import (
    ProjectEndedBeforeResponse,
    StudentPublicationByMajorYearResponse,
    TopFundedProjectResponse,
    TopMentorPublicationResponse,
    TopPublicationYearResponse,
)


def year_to_int(year_value: object) -> int:
    return int(year_value)


async def get_top_funded_projects(
    db: AsyncSession,
) -> list[TopFundedProjectResponse]:
    total_funding = func.sum(Grant.budget).label("total_funding")
    grant_count = func.count(Grant.gid).label("grant_count")

    result = await db.execute(
        select(Project.pid, Project.title, total_funding, grant_count)
        .join(Grant, Grant.pid == Project.pid)
        .group_by(Project.pid, Project.title)
        .order_by(total_funding.desc())
        .limit(5)
    )

    return [
        TopFundedProjectResponse(
            pid=pid,
            title=title,
            total_funding=funding or Decimal("0"),
            grant_count=count or 0,
        )
        for pid, title, funding, count in result.all()
    ]


async def get_top_mentors_by_publications(
    db: AsyncSession,
) -> list[TopMentorPublicationResponse]:
    mentor = aliased(LabMember)
    mentee = aliased(LabMember)
    mentee_pub_count = func.count(Publication.pubid).label("mentee_pub_count")

    result = await db.execute(
        select(mentor.mid, mentor.name, mentee_pub_count)
        .join(mentee, mentee.mentor == mentor.mid)
        .join(Publishes, Publishes.mid == mentee.mid)
        .join(Publication, Publication.pubid == Publishes.pubid)
        .group_by(mentor.mid, mentor.name)
        .order_by(mentee_pub_count.desc())
    )

    return [
        TopMentorPublicationResponse(
            mentor_mid=mentor_mid,
            mentor_name=mentor_name,
            mentee_pub_count=count or 0,
        )
        for mentor_mid, mentor_name, count in result.all()
    ]


async def get_student_publications_by_major_year(
    db: AsyncSession,
) -> list[StudentPublicationByMajorYearResponse]:
    publication_year = func.extract("year", Publication.date).label("publication_year")
    pub_count = func.count(Publication.pubid).label("pub_count")

    result = await db.execute(
        select(Student.major, publication_year, pub_count)
        .join(Publishes, Publishes.mid == Student.mid)
        .join(Publication, Publication.pubid == Publishes.pubid)
        .where(Publication.date.is_not(None), Student.major.is_not(None))
        .group_by(Student.major, publication_year)
        .order_by(Student.major.asc(), publication_year.asc())
    )

    return [
        StudentPublicationByMajorYearResponse(
            major=major,
            year=year_to_int(year),
            pub_count=count or 0,
        )
        for major, year, count in result.all()
    ]


async def get_projects_ended_before(
    db: AsyncSession,
    target_date: date,
) -> list[ProjectEndedBeforeResponse]:
    grant_count = func.count(Grant.gid).label("grant_count")

    result = await db.execute(
        select(Project.pid, Project.title, Project.e_date, grant_count)
        .outerjoin(Grant, Grant.pid == Project.pid)
        .where(Project.e_date.is_not(None), Project.e_date < target_date)
        .group_by(Project.pid, Project.title, Project.e_date)
        .order_by(Project.e_date.desc())
    )

    return [
        ProjectEndedBeforeResponse(
            pid=pid,
            title=title,
            e_date=e_date,
            grant_count=count or 0,
        )
        for pid, title, e_date, count in result.all()
    ]


async def get_top_publication_years(
    db: AsyncSession,
) -> list[TopPublicationYearResponse]:
    publication_year = func.extract("year", Publication.date).label("publication_year")
    pub_count = func.count(Publication.pubid).label("pub_count")

    result = await db.execute(
        select(publication_year, pub_count)
        .join(Publishes, Publishes.pubid == Publication.pubid)
        .join(Student, Student.mid == Publishes.mid)
        .where(Publication.date.is_not(None))
        .group_by(publication_year)
        .order_by(pub_count.desc())
        .limit(3)
    )

    return [
        TopPublicationYearResponse(year=year_to_int(year), pub_count=count or 0)
        for year, count in result.all()
    ]
