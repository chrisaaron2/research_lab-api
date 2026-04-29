from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Grant, LabMember, Project, Works
from app.schemas.project import (
    ProjectCreate,
    ProjectDetailResponse,
    ProjectResponse,
    ProjectStatusFilter,
    ProjectStatusResponse,
    ProjectUpdate,
)


def project_to_response(project: Project) -> ProjectResponse:
    return ProjectResponse(
        pid=project.pid,
        title=project.title,
        s_date=project.s_date,
        e_date=project.e_date,
        e_duration=project.e_duration,
        leader=project.leader,
        leader_name=project.leader_member.name if project.leader_member else None,
    )


async def validate_leader(db: AsyncSession, leader: int | None) -> None:
    if leader is None:
        return

    result = await db.execute(select(LabMember.mid).where(LabMember.mid == leader))
    if result.scalar_one_or_none() is None:
        raise ValueError("leader member not found")


async def get_project_model(db: AsyncSession, pid: int) -> Project | None:
    result = await db.execute(
        select(Project)
        .options(joinedload(Project.leader_member))
        .where(Project.pid == pid)
        .execution_options(populate_existing=True)
    )
    return result.scalar_one_or_none()


async def list_projects(
    db: AsyncSession,
    status: ProjectStatusFilter | None = None,
) -> list[ProjectResponse]:
    today = date.today()
    query = (
        select(Project)
        .options(joinedload(Project.leader_member))
        .order_by(Project.pid)
    )

    if status == "completed":
        query = query.where(Project.e_date.is_not(None), Project.e_date < today)
    elif status == "active":
        query = query.where(Project.e_date.is_not(None), Project.e_date >= today)
    elif status == "ongoing":
        query = query.where(Project.e_date.is_(None))

    result = await db.execute(query)
    projects = result.scalars().all()
    return [project_to_response(project) for project in projects]


async def get_project_detail(
    db: AsyncSession,
    pid: int,
) -> ProjectDetailResponse | None:
    project = await get_project_model(db, pid)
    if project is None:
        return None

    member_count = await db.scalar(
        select(func.count()).select_from(Works).where(Works.pid == pid)
    )
    grant_count = await db.scalar(
        select(func.count()).select_from(Grant).where(Grant.pid == pid)
    )
    total_funding = await db.scalar(
        select(func.sum(Grant.budget)).select_from(Grant).where(Grant.pid == pid)
    )

    base = project_to_response(project).model_dump()
    return ProjectDetailResponse(
        **base,
        member_count=member_count or 0,
        grant_count=grant_count or 0,
        total_funding=total_funding or Decimal("0"),
    )


async def create_project(
    db: AsyncSession,
    payload: ProjectCreate,
) -> ProjectResponse:
    await validate_leader(db, payload.leader)

    try:
        project = Project(
            title=payload.title,
            s_date=payload.s_date,
            e_date=payload.e_date,
            e_duration=payload.e_duration,
            leader=payload.leader,
        )
        db.add(project)
        await db.flush()
        created_pid = project.pid
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ValueError(
            "project could not be created because a foreign key constraint failed"
        ) from exc
    except Exception:
        await db.rollback()
        raise

    created = await get_project_model(db, created_pid)
    if created is None:
        raise RuntimeError("created project could not be loaded")
    return project_to_response(created)


async def update_project(
    db: AsyncSession,
    pid: int,
    payload: ProjectUpdate,
) -> ProjectResponse | None:
    project = await get_project_model(db, pid)
    if project is None:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    if "leader" in update_data:
        await validate_leader(db, update_data["leader"])

    try:
        for field in ("title", "s_date", "e_date", "e_duration", "leader"):
            if field in update_data:
                setattr(project, field, update_data[field])

        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ValueError(
            "project could not be updated because a foreign key constraint failed"
        ) from exc
    except Exception:
        await db.rollback()
        raise

    updated = await get_project_model(db, pid)
    if updated is None:
        raise RuntimeError("updated project could not be loaded")
    return project_to_response(updated)


async def get_project_dependency_counts(db: AsyncSession, pid: int) -> dict[str, int]:
    works_count = await db.scalar(
        select(func.count()).select_from(Works).where(Works.pid == pid)
    )
    grants_count = await db.scalar(
        select(func.count()).select_from(Grant).where(Grant.pid == pid)
    )
    return {"works": works_count or 0, "grants": grants_count or 0}


async def delete_project(db: AsyncSession, pid: int) -> bool:
    project = await get_project_model(db, pid)
    if project is None:
        return False

    dependency_counts = await get_project_dependency_counts(db, pid)
    blockers = [name for name, count in dependency_counts.items() if count > 0]
    if blockers:
        blocker_text = ", ".join(blockers)
        raise ValueError(
            "project cannot be deleted because dependent records exist: "
            f"{blocker_text}"
        )

    try:
        await db.delete(project)
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    return True


async def get_project_status(
    db: AsyncSession,
    pid: int,
) -> ProjectStatusResponse | None:
    project = await get_project_model(db, pid)
    if project is None:
        return None

    today = date.today()
    if project.e_date is None:
        status = "Ongoing (no end date)"
        days_remaining = None
    elif project.e_date < today:
        status = "Completed"
        days_remaining = 0
    else:
        status = "Active"
        days_remaining = (project.e_date - today).days

    return ProjectStatusResponse(
        pid=project.pid,
        title=project.title,
        s_date=project.s_date,
        e_date=project.e_date,
        status=status,
        days_remaining=days_remaining,
    )
