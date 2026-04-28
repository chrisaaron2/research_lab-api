import enum
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.equipment import Uses
    from app.models.project import Project, Works
    from app.models.publication import Publishes


class MemberType(str, enum.Enum):
    student = "student"
    collaborator = "collaborator"
    faculty = "faculty"


class LabMember(Base):
    __tablename__ = "lab_member"

    mid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    join_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    type: Mapped[MemberType] = mapped_column(Enum(MemberType), nullable=False)
    mentor: Mapped[int | None] = mapped_column(
        ForeignKey("lab_member.mid"),
        nullable=True,
    )
    m_sdate: Mapped[date | None] = mapped_column(Date, nullable=True)
    m_edate: Mapped[date | None] = mapped_column(Date, nullable=True)

    mentor_member: Mapped["LabMember | None"] = relationship(
        "LabMember",
        back_populates="mentees",
        remote_side=[mid],
    )
    mentees: Mapped[list["LabMember"]] = relationship(
        "LabMember",
        back_populates="mentor_member",
    )
    student: Mapped["Student | None"] = relationship(
        back_populates="member",
        uselist=False,
    )
    collaborator: Mapped["Collaborator | None"] = relationship(
        back_populates="member",
        uselist=False,
    )
    faculty: Mapped["Faculty | None"] = relationship(
        back_populates="member",
        uselist=False,
    )
    led_projects: Mapped[list["Project"]] = relationship(
        "Project",
        back_populates="leader_member",
        foreign_keys="Project.leader",
    )
    works: Mapped[list["Works"]] = relationship(back_populates="member")
    uses: Mapped[list["Uses"]] = relationship(back_populates="member")
    publishes: Mapped[list["Publishes"]] = relationship(back_populates="member")

    def __repr__(self) -> str:
        return f"LabMember(mid={self.mid!r}, name={self.name!r})"


class Student(Base):
    __tablename__ = "student"

    mid: Mapped[int] = mapped_column(ForeignKey("lab_member.mid"), primary_key=True)
    sid: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    level: Mapped[str | None] = mapped_column(String, nullable=True)
    major: Mapped[str | None] = mapped_column(String, nullable=True)

    member: Mapped[LabMember] = relationship(back_populates="student")

    def __repr__(self) -> str:
        return f"Student(mid={self.mid!r}, sid={self.sid!r})"


class Collaborator(Base):
    __tablename__ = "collaborator"

    mid: Mapped[int] = mapped_column(ForeignKey("lab_member.mid"), primary_key=True)
    affiliation: Mapped[str | None] = mapped_column(String, nullable=True)
    cv: Mapped[str | None] = mapped_column(String, nullable=True)

    member: Mapped[LabMember] = relationship(back_populates="collaborator")

    def __repr__(self) -> str:
        return f"Collaborator(mid={self.mid!r})"


class Faculty(Base):
    __tablename__ = "faculty"

    mid: Mapped[int] = mapped_column(ForeignKey("lab_member.mid"), primary_key=True)
    department: Mapped[str | None] = mapped_column(String, nullable=True)

    member: Mapped[LabMember] = relationship(back_populates="faculty")

    def __repr__(self) -> str:
        return f"Faculty(mid={self.mid!r})"
