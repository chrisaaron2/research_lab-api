from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models import MemberType


class MemberCreate(BaseModel):
    name: str
    join_date: date | None = None
    type: MemberType
    mentor: int | None = None
    m_sdate: date | None = None
    m_edate: date | None = None
    sid: str | None = None
    level: str | None = None
    major: str | None = None
    affiliation: str | None = None
    cv: str | None = None
    department: str | None = None

    @model_validator(mode="after")
    def validate_subtype_fields(self) -> "MemberCreate":
        if self.type == MemberType.student and not self.sid:
            raise ValueError("student members require sid")
        if self.type == MemberType.collaborator and not self.affiliation:
            raise ValueError("collaborator members require affiliation")
        if self.type == MemberType.faculty and not self.department:
            raise ValueError("faculty members require department")
        return self


class MemberUpdate(BaseModel):
    name: str | None = None
    join_date: date | None = None
    mentor: int | None = Field(default=None)
    m_sdate: date | None = None
    m_edate: date | None = None
    sid: str | None = None
    level: str | None = None
    major: str | None = None
    affiliation: str | None = None
    cv: str | None = None
    department: str | None = None


class MemberSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mid: int
    name: str
    type: MemberType


class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mid: int
    name: str
    join_date: date | None
    type: MemberType
    mentor: int | None
    m_sdate: date | None
    m_edate: date | None
    sid: str | None = None
    level: str | None = None
    major: str | None = None
    affiliation: str | None = None
    cv: str | None = None
    department: str | None = None


class DeleteResponse(BaseModel):
    message: str


class MentorshipResponse(BaseModel):
    mentor_mid: int
    mentor_name: str
    mentee_mid: int
    mentee_name: str
