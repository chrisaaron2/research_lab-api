from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict

ProjectStatusFilter = Literal["active", "completed", "ongoing"]


class ProjectCreate(BaseModel):
    title: str
    s_date: date | None = None
    e_date: date | None = None
    e_duration: str | None = None
    leader: int | None = None


class ProjectUpdate(BaseModel):
    title: str | None = None
    s_date: date | None = None
    e_date: date | None = None
    e_duration: str | None = None
    leader: int | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pid: int
    title: str
    s_date: date | None
    e_date: date | None
    e_duration: str | None
    leader: int | None
    leader_name: str | None = None


class ProjectDetailResponse(ProjectResponse):
    member_count: int
    grant_count: int
    total_funding: Decimal


class ProjectStatusResponse(BaseModel):
    pid: int
    title: str
    s_date: date | None
    e_date: date | None
    status: str
    days_remaining: int | None


class DeleteResponse(BaseModel):
    message: str
