from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Grant, Project
from app.schemas.grant import GrantCreate, GrantResponse, GrantUpdate


def grant_to_response(grant: Grant) -> GrantResponse:
    return GrantResponse(
        gid=grant.gid,
        p_duration=grant.p_duration,
        agency=grant.agency,
        budget=grant.budget,
        start_date=grant.start_date,
        pid=grant.pid,
        project_title=grant.project.title if grant.project else None,
    )


async def project_exists(db: AsyncSession, pid: int) -> bool:
    result = await db.execute(select(Project.pid).where(Project.pid == pid))
    return result.scalar_one_or_none() is not None


async def get_grant_model(db: AsyncSession, gid: int) -> Grant | None:
    result = await db.execute(
        select(Grant)
        .options(joinedload(Grant.project))
        .where(Grant.gid == gid)
        .execution_options(populate_existing=True)
    )
    return result.scalar_one_or_none()


async def list_grants(
    db: AsyncSession,
    pid: int | None = None,
    agency: str | None = None,
) -> list[GrantResponse]:
    query = select(Grant).options(joinedload(Grant.project)).order_by(Grant.gid)

    if pid is not None:
        query = query.where(Grant.pid == pid)
    if agency is not None:
        query = query.where(Grant.agency == agency)

    result = await db.execute(query)
    return [grant_to_response(grant) for grant in result.scalars().all()]


async def get_grant(db: AsyncSession, gid: int) -> GrantResponse | None:
    grant = await get_grant_model(db, gid)
    if grant is None:
        return None
    return grant_to_response(grant)


async def create_grant(
    db: AsyncSession,
    payload: GrantCreate,
) -> GrantResponse:
    if not await project_exists(db, payload.pid):
        raise ValueError("project not found")

    grant = Grant(**payload.model_dump())
    db.add(grant)

    try:
        await db.flush()
        created_gid = grant.gid
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ValueError(
            "grant could not be created because a constraint failed"
        ) from exc
    except Exception:
        await db.rollback()
        raise

    created = await get_grant_model(db, created_gid)
    if created is None:
        raise RuntimeError("created grant could not be loaded")
    return grant_to_response(created)


async def update_grant(
    db: AsyncSession,
    gid: int,
    payload: GrantUpdate,
) -> GrantResponse | None:
    grant = await get_grant_model(db, gid)
    if grant is None:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    if "pid" in update_data and not await project_exists(db, update_data["pid"]):
        raise ValueError("project not found")

    for field, value in update_data.items():
        setattr(grant, field, value)

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ValueError(
            "grant could not be updated because a constraint failed"
        ) from exc
    except Exception:
        await db.rollback()
        raise

    updated = await get_grant_model(db, gid)
    if updated is None:
        raise RuntimeError("updated grant could not be loaded")
    return grant_to_response(updated)


async def delete_grant(db: AsyncSession, gid: int) -> bool:
    grant = await get_grant_model(db, gid)
    if grant is None:
        return False

    try:
        await db.delete(grant)
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    return True
