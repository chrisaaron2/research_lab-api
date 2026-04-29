from datetime import date

from pydantic import BaseModel, ConfigDict


class EquipmentCreate(BaseModel):
    e_type: str | None = None
    e_name: str | None = None
    manual: str | None = None


class EquipmentUpdate(BaseModel):
    e_type: str | None = None
    e_name: str | None = None
    manual: str | None = None


class EquipmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    eid: int
    e_type: str | None
    e_name: str | None
    manual: str | None
    device_count: int
    active_device_count: int


class EquipmentDetailResponse(EquipmentResponse):
    usage_count: int


class DeviceCreate(BaseModel):
    eid: int
    status: str | None = None
    p_date: date | None = None


class DeviceUpdate(BaseModel):
    eid: int | None = None
    status: str | None = None
    p_date: date | None = None


class DeviceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    did: int
    eid: int
    equipment_name: str | None
    status: str | None
    p_date: date | None


class DeviceDetailResponse(DeviceResponse):
    equipment_type: str | None
    active_user_count: int


class UsageCreate(BaseModel):
    mid: int
    did: int
    eid: int
    s_date: date | None = None
    e_date: date | None = None
    purpose: str | None = None


class UsageUpdate(BaseModel):
    s_date: date | None = None
    e_date: date | None = None
    purpose: str | None = None


class UsageResponse(BaseModel):
    mid: int
    member_name: str
    did: int
    eid: int
    equipment_name: str | None
    s_date: date | None
    e_date: date | None
    purpose: str | None


class ActiveUserProjectResponse(BaseModel):
    pid: int
    title: str
    role: str | None


class ActiveEquipmentUserResponse(BaseModel):
    mid: int
    member_name: str
    did: int
    purpose: str | None
    active_since: date | None
    projects: list[ActiveUserProjectResponse]


class DeleteResponse(BaseModel):
    message: str
