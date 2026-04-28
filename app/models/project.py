from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.lab_member import LabMember


class Project(Base):
    __tablename__ = "project"

    pid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    s_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    e_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    e_duration: Mapped[str | None] = mapped_column(String, nullable=True)
    leader: Mapped[int | None] = mapped_column(
        ForeignKey("lab_member.mid"),
        nullable=True,
    )

    leader_member: Mapped["LabMember | None"] = relationship(
        "LabMember",
        back_populates="led_projects",
        foreign_keys=[leader],
    )
    works: Mapped[list["Works"]] = relationship(back_populates="project")
    grants: Mapped[list["Grant"]] = relationship(back_populates="project")

    def __repr__(self) -> str:
        return f"Project(pid={self.pid!r}, title={self.title!r})"


class Works(Base):
    __tablename__ = "works"

    pid: Mapped[int] = mapped_column(ForeignKey("project.pid"), primary_key=True)
    mid: Mapped[int] = mapped_column(ForeignKey("lab_member.mid"), primary_key=True)
    role: Mapped[str | None] = mapped_column(String, nullable=True)
    hours: Mapped[int | None] = mapped_column(Integer, nullable=True)

    project: Mapped[Project] = relationship(back_populates="works")
    member: Mapped["LabMember"] = relationship(back_populates="works")

    def __repr__(self) -> str:
        return f"Works(pid={self.pid!r}, mid={self.mid!r})"


class Grant(Base):
    __tablename__ = "grant"

    gid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    p_duration: Mapped[str | None] = mapped_column(String, nullable=True)
    agency: Mapped[str] = mapped_column(String, nullable=False)
    budget: Mapped[Decimal | None] = mapped_column(Numeric, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    pid: Mapped[int] = mapped_column(ForeignKey("project.pid"), nullable=False)

    project: Mapped[Project] = relationship(back_populates="grants")

    def __repr__(self) -> str:
        return f"Grant(gid={self.gid!r}, agency={self.agency!r})"
