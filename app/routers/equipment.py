from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_admin
from app.crud.equipment import (
    create_device,
    create_equipment,
    create_usage,
    delete_device,
    delete_equipment,
    delete_usage,
    get_active_equipment_users,
    get_device_detail,
    get_equipment_detail,
    list_devices,
    list_equipment,
    list_usages,
    update_device,
    update_equipment,
    update_usage,
)
from app.db import get_db
from app.schemas.equipment import (
    ActiveEquipmentUserResponse,
    DeleteResponse,
    DeviceCreate,
    DeviceDetailResponse,
    DeviceResponse,
    DeviceUpdate,
    EquipmentCreate,
    EquipmentDetailResponse,
    EquipmentResponse,
    EquipmentUpdate,
    UsageCreate,
    UsageResponse,
    UsageUpdate,
)


router = APIRouter(tags=["equipment"])


@router.get("/equipment", response_model=list[EquipmentResponse])
async def read_equipment(
    db: Annotated[AsyncSession, Depends(get_db)],
    e_type: str | None = None,
    status: str | None = None,
) -> list[EquipmentResponse]:
    return await list_equipment(db, e_type=e_type, status=status)


@router.get(
    "/equipment/{eid}/active-users",
    response_model=list[ActiveEquipmentUserResponse],
)
async def read_active_equipment_users(
    eid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[ActiveEquipmentUserResponse]:
    users = await get_active_equipment_users(db, eid)
    if users is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="equipment not found",
        )
    return users


@router.get("/equipment/{eid}", response_model=EquipmentDetailResponse)
async def read_equipment_detail(
    eid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> EquipmentDetailResponse:
    equipment = await get_equipment_detail(db, eid)
    if equipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="equipment not found",
        )
    return equipment


@router.post(
    "/equipment",
    response_model=EquipmentResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def create_equipment_route(
    payload: EquipmentCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> EquipmentResponse:
    return await create_equipment(db, payload)


@router.put(
    "/equipment/{eid}",
    response_model=EquipmentResponse,
    dependencies=[Depends(require_admin)],
)
async def update_equipment_route(
    eid: int,
    payload: EquipmentUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> EquipmentResponse:
    equipment = await update_equipment(db, eid, payload)
    if equipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="equipment not found",
        )
    return equipment


@router.delete(
    "/equipment/{eid}",
    response_model=DeleteResponse,
    dependencies=[Depends(require_admin)],
)
async def delete_equipment_route(
    eid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeleteResponse:
    try:
        deleted = await delete_equipment(db, eid)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="equipment not found",
        )
    return DeleteResponse(message="equipment deleted")


@router.get("/devices", response_model=list[DeviceResponse])
async def read_devices(
    db: Annotated[AsyncSession, Depends(get_db)],
    eid: int | None = None,
    status: str | None = None,
) -> list[DeviceResponse]:
    return await list_devices(db, eid=eid, status=status)


@router.get("/devices/{did}", response_model=DeviceDetailResponse)
async def read_device_detail(
    did: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeviceDetailResponse:
    device = await get_device_detail(db, did)
    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="device not found",
        )
    return device


@router.post(
    "/devices",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def create_device_route(
    payload: DeviceCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeviceResponse:
    try:
        return await create_device(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.put(
    "/devices/{did}",
    response_model=DeviceResponse,
    dependencies=[Depends(require_admin)],
)
async def update_device_route(
    did: int,
    payload: DeviceUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeviceResponse:
    try:
        device = await update_device(db, did, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if device is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="device not found",
        )
    return device


@router.delete(
    "/devices/{did}",
    response_model=DeleteResponse,
    dependencies=[Depends(require_admin)],
)
async def delete_device_route(
    did: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeleteResponse:
    try:
        deleted = await delete_device(db, did)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="device not found",
        )
    return DeleteResponse(message="device deleted")


@router.get("/uses", response_model=list[UsageResponse])
async def read_usages(
    db: Annotated[AsyncSession, Depends(get_db)],
    mid: int | None = None,
    did: int | None = None,
    eid: int | None = None,
    active_only: bool = False,
) -> list[UsageResponse]:
    return await list_usages(
        db,
        mid=mid,
        did=did,
        eid=eid,
        active_only=active_only,
    )


@router.post(
    "/uses",
    response_model=UsageResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def create_usage_route(
    payload: UsageCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UsageResponse:
    try:
        return await create_usage(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.put(
    "/uses/{mid}/{did}/{eid}",
    response_model=UsageResponse,
    dependencies=[Depends(require_admin)],
)
async def update_usage_route(
    mid: int,
    did: int,
    eid: int,
    payload: UsageUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> UsageResponse:
    usage = await update_usage(db, mid, did, eid, payload)
    if usage is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="usage not found",
        )
    return usage


@router.delete(
    "/uses/{mid}/{did}/{eid}",
    response_model=DeleteResponse,
    dependencies=[Depends(require_admin)],
)
async def delete_usage_route(
    mid: int,
    did: int,
    eid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeleteResponse:
    deleted = await delete_usage(db, mid, did, eid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="usage not found",
        )
    return DeleteResponse(message="usage deleted")
