from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.lab_member import LabMember


class Publication(Base):
    __tablename__ = "publication"

    pubid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    venue: Mapped[str | None] = mapped_column(String, nullable=True)
    date: Mapped[date | None] = mapped_column(Date, nullable=True)
    doi: Mapped[str | None] = mapped_column(String, nullable=True)

    publishes: Mapped[list["Publishes"]] = relationship(back_populates="publication")

    def __repr__(self) -> str:
        return f"Publication(pubid={self.pubid!r}, title={self.title!r})"


class Publishes(Base):
    __tablename__ = "publishes"

    mid: Mapped[int] = mapped_column(ForeignKey("lab_member.mid"), primary_key=True)
    pubid: Mapped[int] = mapped_column(
        ForeignKey("publication.pubid"),
        primary_key=True,
    )

    member: Mapped["LabMember"] = relationship(back_populates="publishes")
    publication: Mapped[Publication] = relationship(back_populates="publishes")

    def __repr__(self) -> str:
        return f"Publishes(mid={self.mid!r}, pubid={self.pubid!r})"
