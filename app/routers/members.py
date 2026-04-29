from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_admin
from app.crud.members import (
    create_member,
    delete_member,
    get_member,
    get_members_for_grant,
    get_project_mentorships,
    list_members,
    update_member,
)
from app.db import get_db
from app.models import MemberType
from app.schemas.member import (
    DeleteResponse,
    MemberCreate,
    MemberResponse,
    MemberSummary,
    MemberUpdate,
    MentorshipResponse,
)


router = APIRouter(tags=["members"])


@router.get("/members", response_model=list[MemberResponse])
async def read_members(
    db: Annotated[AsyncSession, Depends(get_db)],
    type: MemberType | None = None,
) -> list[MemberResponse]:
    return await list_members(db, type)


@router.get("/members/{mid}", response_model=MemberResponse)
async def read_member(
    mid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> MemberResponse:
    member = await get_member(db, mid)
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="member not found",
        )
    return member


@router.post(
    "/members",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def create_member_route(
    payload: MemberCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> MemberResponse:
    try:
        return await create_member(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.put(
    "/members/{mid}",
    response_model=MemberResponse,
    dependencies=[Depends(require_admin)],
)
async def update_member_route(
    mid: int,
    payload: MemberUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> MemberResponse:
    try:
        member = await update_member(db, mid, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="member not found",
        )
    return member


@router.delete(
    "/members/{mid}",
    response_model=DeleteResponse,
    dependencies=[Depends(require_admin)],
)
async def delete_member_route(
    mid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeleteResponse:
    try:
        deleted = await delete_member(db, mid)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="member not found",
        )
    return DeleteResponse(message="member deleted")


@router.get("/grants/{gid}/members", response_model=list[MemberSummary])
async def read_members_for_grant(
    gid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[MemberSummary]:
    members = await get_members_for_grant(db, gid)
    if members is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="grant not found",
        )
    return members


@router.get("/projects/{pid}/mentorships", response_model=list[MentorshipResponse])
async def read_project_mentorships(
    pid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[MentorshipResponse]:
    mentorships = await get_project_mentorships(db, pid)
    if mentorships is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="project not found",
        )
    return mentorships
