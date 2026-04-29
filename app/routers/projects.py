from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.projects import (
    create_project,
    delete_project,
    get_project_detail,
    get_project_status,
    list_projects,
    update_project,
)
from app.db import get_db
from app.schemas.project import (
    DeleteResponse,
    ProjectCreate,
    ProjectDetailResponse,
    ProjectResponse,
    ProjectStatusFilter,
    ProjectStatusResponse,
    ProjectUpdate,
)


router = APIRouter(tags=["projects"])


async def require_admin_placeholder() -> None:
    return None


@router.get("/projects", response_model=list[ProjectResponse])
async def read_projects(
    db: Annotated[AsyncSession, Depends(get_db)],
    status: ProjectStatusFilter | None = None,
) -> list[ProjectResponse]:
    return await list_projects(db, status)


@router.get("/projects/{pid}/status", response_model=ProjectStatusResponse)
async def read_project_status(
    pid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProjectStatusResponse:
    project_status = await get_project_status(db, pid)
    if project_status is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="project not found",
        )
    return project_status


@router.get("/projects/{pid}", response_model=ProjectDetailResponse)
async def read_project(
    pid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProjectDetailResponse:
    project = await get_project_detail(db, pid)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="project not found",
        )
    return project


@router.post(
    "/projects",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin_placeholder)],
)
async def create_project_route(
    payload: ProjectCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProjectResponse:
    try:
        return await create_project(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.put(
    "/projects/{pid}",
    response_model=ProjectResponse,
    dependencies=[Depends(require_admin_placeholder)],
)
async def update_project_route(
    pid: int,
    payload: ProjectUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ProjectResponse:
    try:
        project = await update_project(db, pid, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="project not found",
        )
    return project


@router.delete(
    "/projects/{pid}",
    response_model=DeleteResponse,
    dependencies=[Depends(require_admin_placeholder)],
)
async def delete_project_route(
    pid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeleteResponse:
    try:
        deleted = await delete_project(db, pid)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="project not found",
        )
    return DeleteResponse(message="project deleted")
