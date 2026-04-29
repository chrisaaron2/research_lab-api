from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models import Device, Equipment, LabMember, Project, Uses, Works
from app.schemas.equipment import (
    ActiveEquipmentUserResponse,
    ActiveUserProjectResponse,
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


def equipment_load_query():
    return select(Equipment).order_by(Equipment.eid)


async def equipment_exists(db: AsyncSession, eid: int) -> bool:
    result = await db.execute(select(Equipment.eid).where(Equipment.eid == eid))
    return result.scalar_one_or_none() is not None


async def member_exists(db: AsyncSession, mid: int) -> bool:
    result = await db.execute(select(LabMember.mid).where(LabMember.mid == mid))
    return result.scalar_one_or_none() is not None


async def get_equipment_model(db: AsyncSession, eid: int) -> Equipment | None:
    result = await db.execute(select(Equipment).where(Equipment.eid == eid))
    return result.scalar_one_or_none()


async def get_device_model(db: AsyncSession, did: int) -> Device | None:
    result = await db.execute(
        select(Device)
        .options(joinedload(Device.equipment))
        .where(Device.did == did)
        .execution_options(populate_existing=True)
    )
    return result.scalar_one_or_none()


async def get_usage_model(
    db: AsyncSession,
    mid: int,
    did: int,
    eid: int,
) -> Uses | None:
    result = await db.execute(
        select(Uses)
        .options(joinedload(Uses.member), joinedload(Uses.equipment))
        .where(Uses.mid == mid, Uses.did == did, Uses.eid == eid)
        .execution_options(populate_existing=True)
    )
    return result.scalar_one_or_none()


async def equipment_to_response(
    db: AsyncSession,
    equipment: Equipment,
) -> EquipmentResponse:
    device_count = await db.scalar(
        select(func.count()).select_from(Device).where(Device.eid == equipment.eid)
    )
    active_device_count = await db.scalar(
        select(func.count())
        .select_from(Device)
        .where(Device.eid == equipment.eid, Device.status == "active")
    )
    return EquipmentResponse(
        eid=equipment.eid,
        e_type=equipment.e_type,
        e_name=equipment.e_name,
        manual=equipment.manual,
        device_count=device_count or 0,
        active_device_count=active_device_count or 0,
    )


async def equipment_to_detail(
    db: AsyncSession,
    equipment: Equipment,
) -> EquipmentDetailResponse:
    base = (await equipment_to_response(db, equipment)).model_dump()
    usage_count = await db.scalar(
        select(func.count()).select_from(Uses).where(Uses.eid == equipment.eid)
    )
    return EquipmentDetailResponse(**base, usage_count=usage_count or 0)


def device_to_response(device: Device) -> DeviceResponse:
    return DeviceResponse(
        did=device.did,
        eid=device.eid,
        equipment_name=device.equipment.e_name if device.equipment else None,
        status=device.status,
        p_date=device.p_date,
    )


async def device_to_detail(db: AsyncSession, device: Device) -> DeviceDetailResponse:
    active_user_count = await db.scalar(
        select(func.count())
        .select_from(Uses)
        .where(Uses.did == device.did, Uses.e_date.is_(None))
    )
    base = device_to_response(device).model_dump()
    return DeviceDetailResponse(
        **base,
        equipment_type=device.equipment.e_type if device.equipment else None,
        active_user_count=active_user_count or 0,
    )


def usage_to_response(usage: Uses) -> UsageResponse:
    return UsageResponse(
        mid=usage.mid,
        member_name=usage.member.name,
        did=usage.did,
        eid=usage.eid,
        equipment_name=usage.equipment.e_name,
        s_date=usage.s_date,
        e_date=usage.e_date,
        purpose=usage.purpose,
    )


async def list_equipment(
    db: AsyncSession,
    e_type: str | None = None,
    status: str | None = None,
) -> list[EquipmentResponse]:
    query = equipment_load_query()
    if e_type is not None:
        query = query.where(Equipment.e_type == e_type)
    if status is not None:
        query = query.join(Device).where(Device.status == status).distinct()

    result = await db.execute(query)
    equipment_items = result.scalars().all()
    return [await equipment_to_response(db, item) for item in equipment_items]


async def get_equipment_detail(
    db: AsyncSession,
    eid: int,
) -> EquipmentDetailResponse | None:
    equipment = await get_equipment_model(db, eid)
    if equipment is None:
        return None
    return await equipment_to_detail(db, equipment)


async def create_equipment(
    db: AsyncSession,
    payload: EquipmentCreate,
) -> EquipmentResponse:
    try:
        equipment = Equipment(
            e_type=payload.e_type,
            e_name=payload.e_name,
            manual=payload.manual,
        )
        db.add(equipment)
        await db.flush()
        created_eid = equipment.eid
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    created = await get_equipment_model(db, created_eid)
    if created is None:
        raise RuntimeError("created equipment could not be loaded")
    return await equipment_to_response(db, created)


async def update_equipment(
    db: AsyncSession,
    eid: int,
    payload: EquipmentUpdate,
) -> EquipmentResponse | None:
    equipment = await get_equipment_model(db, eid)
    if equipment is None:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    try:
        for field in ("e_type", "e_name", "manual"):
            if field in update_data:
                setattr(equipment, field, update_data[field])
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    updated = await get_equipment_model(db, eid)
    if updated is None:
        raise RuntimeError("updated equipment could not be loaded")
    return await equipment_to_response(db, updated)


async def delete_equipment(db: AsyncSession, eid: int) -> bool:
    equipment = await get_equipment_model(db, eid)
    if equipment is None:
        return False

    device_count = await db.scalar(
        select(func.count()).select_from(Device).where(Device.eid == eid)
    )
    usage_count = await db.scalar(
        select(func.count()).select_from(Uses).where(Uses.eid == eid)
    )
    blockers = []
    if device_count:
        blockers.append("devices")
    if usage_count:
        blockers.append("uses")
    if blockers:
        raise ValueError(
            "equipment cannot be deleted because dependent records exist: "
            f"{', '.join(blockers)}"
        )

    try:
        await db.delete(equipment)
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    return True


async def list_devices(
    db: AsyncSession,
    eid: int | None = None,
    status: str | None = None,
) -> list[DeviceResponse]:
    query = (
        select(Device)
        .options(joinedload(Device.equipment))
        .order_by(Device.did)
    )
    if eid is not None:
        query = query.where(Device.eid == eid)
    if status is not None:
        query = query.where(Device.status == status)

    result = await db.execute(query)
    devices = result.scalars().all()
    return [device_to_response(device) for device in devices]


async def get_device_detail(
    db: AsyncSession,
    did: int,
) -> DeviceDetailResponse | None:
    device = await get_device_model(db, did)
    if device is None:
        return None
    return await device_to_detail(db, device)


async def create_device(db: AsyncSession, payload: DeviceCreate) -> DeviceResponse:
    if not await equipment_exists(db, payload.eid):
        raise ValueError("equipment not found")

    try:
        device = Device(eid=payload.eid, status=payload.status, p_date=payload.p_date)
        db.add(device)
        await db.flush()
        created_did = device.did
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ValueError(
            "device could not be created because a foreign key constraint failed"
        ) from exc
    except Exception:
        await db.rollback()
        raise

    created = await get_device_model(db, created_did)
    if created is None:
        raise RuntimeError("created device could not be loaded")
    return device_to_response(created)


async def update_device(
    db: AsyncSession,
    did: int,
    payload: DeviceUpdate,
) -> DeviceResponse | None:
    device = await get_device_model(db, did)
    if device is None:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    if "eid" in update_data and update_data["eid"] != device.eid:
        usage_count = await db.scalar(
            select(func.count()).select_from(Uses).where(Uses.did == did)
        )
        if usage_count:
            raise ValueError(
                "device equipment cannot be changed while usage records exist"
            )
        if not await equipment_exists(db, update_data["eid"]):
            raise ValueError("equipment not found")

    try:
        for field in ("eid", "status", "p_date"):
            if field in update_data:
                setattr(device, field, update_data[field])
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ValueError(
            "device could not be updated because a foreign key constraint failed"
        ) from exc
    except Exception:
        await db.rollback()
        raise

    updated = await get_device_model(db, did)
    if updated is None:
        raise RuntimeError("updated device could not be loaded")
    return device_to_response(updated)


async def delete_device(db: AsyncSession, did: int) -> bool:
    device = await get_device_model(db, did)
    if device is None:
        return False

    usage_count = await db.scalar(
        select(func.count()).select_from(Uses).where(Uses.did == did)
    )
    if usage_count:
        raise ValueError("device cannot be deleted because uses records exist")

    try:
        await db.delete(device)
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    return True


async def list_usages(
    db: AsyncSession,
    mid: int | None = None,
    did: int | None = None,
    eid: int | None = None,
    active_only: bool = False,
) -> list[UsageResponse]:
    query = (
        select(Uses)
        .options(joinedload(Uses.member), joinedload(Uses.equipment))
        .order_by(Uses.mid, Uses.did, Uses.eid)
    )
    if mid is not None:
        query = query.where(Uses.mid == mid)
    if did is not None:
        query = query.where(Uses.did == did)
    if eid is not None:
        query = query.where(Uses.eid == eid)
    if active_only:
        query = query.where(Uses.e_date.is_(None))

    result = await db.execute(query)
    usages = result.scalars().all()
    return [usage_to_response(usage) for usage in usages]


async def validate_usage_references(
    db: AsyncSession,
    mid: int,
    did: int,
    eid: int,
) -> None:
    if not await member_exists(db, mid):
        raise ValueError("member not found")

    device = await get_device_model(db, did)
    if device is None:
        raise ValueError("device not found")
    if not await equipment_exists(db, eid):
        raise ValueError("equipment not found")
    if device.eid != eid:
        raise ValueError("device does not belong to the provided equipment")


async def create_usage(db: AsyncSession, payload: UsageCreate) -> UsageResponse:
    await validate_usage_references(db, payload.mid, payload.did, payload.eid)
    existing = await get_usage_model(db, payload.mid, payload.did, payload.eid)
    if existing is not None:
        raise ValueError("usage record already exists")

    try:
        usage = Uses(
            mid=payload.mid,
            did=payload.did,
            eid=payload.eid,
            s_date=payload.s_date,
            e_date=payload.e_date,
            purpose=payload.purpose,
        )
        db.add(usage)
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ValueError(
            "usage could not be created because a constraint failed"
        ) from exc
    except Exception:
        await db.rollback()
        raise

    created = await get_usage_model(db, payload.mid, payload.did, payload.eid)
    if created is None:
        raise RuntimeError("created usage could not be loaded")
    return usage_to_response(created)


async def update_usage(
    db: AsyncSession,
    mid: int,
    did: int,
    eid: int,
    payload: UsageUpdate,
) -> UsageResponse | None:
    usage = await get_usage_model(db, mid, did, eid)
    if usage is None:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    try:
        for field in ("s_date", "e_date", "purpose"):
            if field in update_data:
                setattr(usage, field, update_data[field])
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    updated = await get_usage_model(db, mid, did, eid)
    if updated is None:
        raise RuntimeError("updated usage could not be loaded")
    return usage_to_response(updated)


async def delete_usage(db: AsyncSession, mid: int, did: int, eid: int) -> bool:
    usage = await get_usage_model(db, mid, did, eid)
    if usage is None:
        return False

    try:
        await db.delete(usage)
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    return True


async def get_active_equipment_users(
    db: AsyncSession,
    eid: int,
) -> list[ActiveEquipmentUserResponse] | None:
    if not await equipment_exists(db, eid):
        return None

    result = await db.execute(
        select(Uses)
        .options(joinedload(Uses.member))
        .where(Uses.eid == eid, Uses.e_date.is_(None))
        .order_by(Uses.mid, Uses.did)
    )
    active_usages = result.scalars().all()

    responses: list[ActiveEquipmentUserResponse] = []
    for usage in active_usages:
        projects_result = await db.execute(
            select(Project.pid, Project.title, Works.role)
            .join(Works, Works.pid == Project.pid)
            .where(Works.mid == usage.mid)
            .order_by(Project.pid)
        )
        projects = [
            ActiveUserProjectResponse(pid=pid, title=title, role=role)
            for pid, title, role in projects_result.all()
        ]
        responses.append(
            ActiveEquipmentUserResponse(
                mid=usage.mid,
                member_name=usage.member.name,
                did=usage.did,
                purpose=usage.purpose,
                active_since=usage.s_date,
                projects=projects,
            )
        )

    return responses
