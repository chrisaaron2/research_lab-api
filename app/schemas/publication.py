from datetime import date as Date

from pydantic import BaseModel, ConfigDict


class PublicationBase(BaseModel):
    title: str
    venue: str | None = None
    date: Date | None = None
    doi: str | None = None


class PublicationCreate(PublicationBase):
    pass


class PublicationUpdate(BaseModel):
    title: str | None = None
    venue: str | None = None
    date: Date | None = None
    doi: str | None = None


class PublicationAuthorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    mid: int
    name: str
    type: str


class PublicationListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pubid: int
    title: str
    venue: str | None
    date: Date | None
    doi: str | None
    author_count: int


class PublicationDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pubid: int
    title: str
    venue: str | None
    date: Date | None
    doi: str | None
    authors: list[PublicationAuthorResponse]


class AuthorshipCreate(BaseModel):
    mid: int


class DeleteResponse(BaseModel):
    message: str
