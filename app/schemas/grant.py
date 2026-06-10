from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class GrantBase(BaseModel):
    p_duration: str | None = None
    agency: str
    budget: Decimal | None = None
    start_date: date | None = None
    pid: int


class GrantCreate(GrantBase):
    pass


class GrantUpdate(BaseModel):
    p_duration: str | None = None
    agency: str | None = None
    budget: Decimal | None = None
    start_date: date | None = None
    pid: int | None = None


class GrantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    gid: int
    p_duration: str | None
    agency: str
    budget: Decimal | None
    start_date: date | None
    pid: int
    project_title: str | None = None


class DeleteResponse(BaseModel):
    message: str
