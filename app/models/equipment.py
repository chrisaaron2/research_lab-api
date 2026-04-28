from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.lab_member import LabMember


class Equipment(Base):
    __tablename__ = "equipment"

    eid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    e_type: Mapped[str | None] = mapped_column(String, nullable=True)
    e_name: Mapped[str | None] = mapped_column(String, nullable=True)
    manual: Mapped[str | None] = mapped_column(String, nullable=True)

    devices: Mapped[list["Device"]] = relationship(back_populates="equipment")
    uses: Mapped[list["Uses"]] = relationship(back_populates="equipment")

    def __repr__(self) -> str:
        return f"Equipment(eid={self.eid!r}, e_name={self.e_name!r})"


class Device(Base):
    __tablename__ = "device"

    did: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    eid: Mapped[int] = mapped_column(ForeignKey("equipment.eid"), nullable=False)
    status: Mapped[str | None] = mapped_column(String, nullable=True)
    p_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    equipment: Mapped[Equipment] = relationship(back_populates="devices")
    uses: Mapped[list["Uses"]] = relationship(back_populates="device")

    def __repr__(self) -> str:
        return f"Device(did={self.did!r}, eid={self.eid!r})"


class Uses(Base):
    __tablename__ = "uses"

    mid: Mapped[int] = mapped_column(ForeignKey("lab_member.mid"), primary_key=True)
    did: Mapped[int] = mapped_column(ForeignKey("device.did"), primary_key=True)
    eid: Mapped[int] = mapped_column(ForeignKey("equipment.eid"), primary_key=True)
    s_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    e_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    purpose: Mapped[str | None] = mapped_column(String, nullable=True)

    member: Mapped["LabMember"] = relationship(back_populates="uses")
    device: Mapped[Device] = relationship(back_populates="uses")
    equipment: Mapped[Equipment] = relationship(back_populates="uses")

    def __repr__(self) -> str:
        return f"Uses(mid={self.mid!r}, did={self.did!r}, eid={self.eid!r})"
