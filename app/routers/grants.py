from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_admin
from app.crud.grants import (
    create_grant,
    delete_grant,
    get_grant,
    list_grants,
    update_grant,
)
from app.db import get_db
from app.schemas.grant import (
    DeleteResponse,
    GrantCreate,
    GrantResponse,
    GrantUpdate,
)

router = APIRouter(tags=["grants"])


@router.get("/grants", response_model=list[GrantResponse])
async def read_grants(
    db: Annotated[AsyncSession, Depends(get_db)],
    pid: int | None = None,
    agency: str | None = None,
) -> list[GrantResponse]:
    return await list_grants(db, pid=pid, agency=agency)


@router.get("/grants/{gid}", response_model=GrantResponse)
async def read_grant(
    gid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> GrantResponse:
    grant = await get_grant(db, gid)
    if grant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="grant not found",
        )
    return grant


@router.post(
    "/grants",
    response_model=GrantResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def create_grant_endpoint(
    payload: GrantCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> GrantResponse:
    try:
        return await create_grant(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.put(
    "/grants/{gid}",
    response_model=GrantResponse,
    dependencies=[Depends(require_admin)],
)
async def update_grant_endpoint(
    gid: int,
    payload: GrantUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> GrantResponse:
    try:
        grant = await update_grant(db, gid, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if grant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="grant not found",
        )
    return grant


@router.delete(
    "/grants/{gid}",
    response_model=DeleteResponse,
    dependencies=[Depends(require_admin)],
)
async def delete_grant_endpoint(
    gid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeleteResponse:
    deleted = await delete_grant(db, gid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="grant not found",
        )
    return DeleteResponse(message="grant deleted")
