from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class TopFundedProjectResponse(BaseModel):
    pid: int
    title: str
    total_funding: Decimal
    grant_count: int


class TopMentorPublicationResponse(BaseModel):
    mentor_mid: int
    mentor_name: str
    mentee_pub_count: int


class StudentPublicationByMajorYearResponse(BaseModel):
    major: str
    year: int
    pub_count: int


class ProjectEndedBeforeResponse(BaseModel):
    pid: int
    title: str
    e_date: date
    grant_count: int


class TopPublicationYearResponse(BaseModel):
    year: int
    pub_count: int
