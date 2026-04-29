from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import (
    Collaborator,
    Faculty,
    Grant,
    LabMember,
    MemberType,
    Project,
    Publishes,
    Student,
    Uses,
    Works,
)
from app.schemas.member import (
    MemberCreate,
    MemberResponse,
    MemberSummary,
    MemberUpdate,
    MentorshipResponse,
)


def member_to_response(member: LabMember) -> MemberResponse:
    response_data = {
        "mid": member.mid,
        "name": member.name,
        "join_date": member.join_date,
        "type": member.type,
        "mentor": member.mentor,
        "m_sdate": member.m_sdate,
        "m_edate": member.m_edate,
    }

    if member.student is not None:
        response_data.update(
            {
                "sid": member.student.sid,
                "level": member.student.level,
                "major": member.student.major,
            }
        )
    if member.collaborator is not None:
        response_data.update(
            {
                "affiliation": member.collaborator.affiliation,
                "cv": member.collaborator.cv,
            }
        )
    if member.faculty is not None:
        response_data["department"] = member.faculty.department

    return MemberResponse(**response_data)


def member_to_summary(member: LabMember) -> MemberSummary:
    return MemberSummary(mid=member.mid, name=member.name, type=member.type)


def member_load_options() -> tuple:
    return (
        selectinload(LabMember.student),
        selectinload(LabMember.collaborator),
        selectinload(LabMember.faculty),
    )


async def list_members(
    db: AsyncSession,
    member_type: MemberType | None = None,
) -> list[MemberResponse]:
    query = select(LabMember).options(*member_load_options()).order_by(LabMember.mid)
    if member_type is not None:
        query = query.where(LabMember.type == member_type)

    result = await db.execute(query)
    members = result.scalars().all()
    return [member_to_response(member) for member in members]


async def get_member(db: AsyncSession, mid: int) -> MemberResponse | None:
    member = await get_member_model(db, mid)
    if member is None:
        return None
    return member_to_response(member)


async def get_member_model(db: AsyncSession, mid: int) -> LabMember | None:
    result = await db.execute(
        select(LabMember).options(*member_load_options()).where(LabMember.mid == mid)
    )
    return result.scalar_one_or_none()


async def member_exists(db: AsyncSession, mid: int) -> bool:
    result = await db.execute(select(LabMember.mid).where(LabMember.mid == mid))
    return result.scalar_one_or_none() is not None


async def validate_mentor(
    db: AsyncSession,
    mentor: int | None,
    current_mid: int | None = None,
) -> None:
    if mentor is not None and mentor == current_mid:
        raise ValueError("member cannot be their own mentor")
    if mentor is not None and not await member_exists(db, mentor):
        raise ValueError("mentor member not found")


async def create_member(db: AsyncSession, payload: MemberCreate) -> MemberResponse:
    await validate_mentor(db, payload.mentor)

    try:
        member = LabMember(
            name=payload.name,
            join_date=payload.join_date,
            type=payload.type,
            mentor=payload.mentor,
            m_sdate=payload.m_sdate,
            m_edate=payload.m_edate,
        )
        db.add(member)
        await db.flush()

        if payload.type == MemberType.student:
            db.add(
                Student(
                    mid=member.mid,
                    sid=payload.sid,
                    level=payload.level,
                    major=payload.major,
                )
            )
        elif payload.type == MemberType.collaborator:
            db.add(
                Collaborator(
                    mid=member.mid,
                    affiliation=payload.affiliation,
                    cv=payload.cv,
                )
            )
        elif payload.type == MemberType.faculty:
            db.add(Faculty(mid=member.mid, department=payload.department))

        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ValueError(
            "member could not be created because a unique or foreign key "
            "constraint failed"
        ) from exc
    except Exception:
        await db.rollback()
        raise

    created = await get_member_model(db, member.mid)
    if created is None:
        raise RuntimeError("created member could not be loaded")
    return member_to_response(created)


async def update_member(
    db: AsyncSession,
    mid: int,
    payload: MemberUpdate,
) -> MemberResponse | None:
    member = await get_member_model(db, mid)
    if member is None:
        return None

    update_data = payload.model_dump(exclude_unset=True)
    if "mentor" in update_data:
        await validate_mentor(db, update_data["mentor"], current_mid=mid)

    try:
        for field in ("name", "join_date", "mentor", "m_sdate", "m_edate"):
            if field in update_data:
                setattr(member, field, update_data[field])

        if member.type == MemberType.student and member.student is not None:
            for field in ("sid", "level", "major"):
                if field in update_data:
                    setattr(member.student, field, update_data[field])
        elif member.type == MemberType.collaborator and member.collaborator is not None:
            for field in ("affiliation", "cv"):
                if field in update_data:
                    setattr(member.collaborator, field, update_data[field])
        elif member.type == MemberType.faculty and member.faculty is not None:
            if "department" in update_data:
                member.faculty.department = update_data["department"]

        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise ValueError(
            "member could not be updated because a unique or foreign key "
            "constraint failed"
        ) from exc
    except Exception:
        await db.rollback()
        raise

    updated = await get_member_model(db, mid)
    if updated is None:
        raise RuntimeError("updated member could not be loaded")
    return member_to_response(updated)


async def get_dependency_counts(db: AsyncSession, mid: int) -> dict[str, int]:
    works_count = await db.scalar(
        select(func.count()).select_from(Works).where(Works.mid == mid)
    )
    uses_count = await db.scalar(
        select(func.count()).select_from(Uses).where(Uses.mid == mid)
    )
    publishes_count = await db.scalar(
        select(func.count()).select_from(Publishes).where(Publishes.mid == mid)
    )
    led_projects_count = await db.scalar(
        select(func.count()).select_from(Project).where(Project.leader == mid)
    )
    mentees_count = await db.scalar(
        select(func.count()).select_from(LabMember).where(LabMember.mentor == mid)
    )
    return {
        "works": works_count or 0,
        "uses": uses_count or 0,
        "publishes": publishes_count or 0,
        "led projects": led_projects_count or 0,
        "mentees": mentees_count or 0,
    }


async def delete_member(db: AsyncSession, mid: int) -> bool:
    member = await get_member_model(db, mid)
    if member is None:
        return False

    dependency_counts = await get_dependency_counts(db, mid)
    blockers = [name for name, count in dependency_counts.items() if count > 0]
    if blockers:
        blocker_text = ", ".join(blockers)
        raise ValueError(
            "member cannot be deleted because dependent records exist: "
            f"{blocker_text}"
        )

    try:
        if member.student is not None:
            await db.delete(member.student)
        if member.collaborator is not None:
            await db.delete(member.collaborator)
        if member.faculty is not None:
            await db.delete(member.faculty)

        await db.delete(member)
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    return True


async def get_members_for_grant(
    db: AsyncSession,
    gid: int,
) -> list[MemberSummary] | None:
    grant_exists = await db.scalar(select(Grant.gid).where(Grant.gid == gid))
    if grant_exists is None:
        return None

    result = await db.execute(
        select(LabMember)
        .join(Works, Works.mid == LabMember.mid)
        .join(Project, Project.pid == Works.pid)
        .join(Grant, Grant.pid == Project.pid)
        .where(Grant.gid == gid)
        .order_by(LabMember.mid)
    )
    members = result.scalars().all()
    return [member_to_summary(member) for member in members]


async def get_project_mentorships(
    db: AsyncSession,
    pid: int,
) -> list[MentorshipResponse] | None:
    project_exists = await db.scalar(select(Project.pid).where(Project.pid == pid))
    if project_exists is None:
        return None

    result = await db.execute(
        select(LabMember)
        .join(Works, Works.mid == LabMember.mid)
        .where(Works.pid == pid)
        .order_by(LabMember.mid)
    )
    members = result.scalars().all()
    members_by_mid = {member.mid: member for member in members}

    mentorships: list[MentorshipResponse] = []
    for mentee in members:
        if mentee.mentor is None:
            continue
        mentor = members_by_mid.get(mentee.mentor)
        if mentor is None:
            continue
        mentorships.append(
            MentorshipResponse(
                mentor_mid=mentor.mid,
                mentor_name=mentor.name,
                mentee_mid=mentee.mid,
                mentee_name=mentee.name,
            )
        )

    return mentorships
