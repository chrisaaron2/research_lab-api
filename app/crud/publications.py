from sqlalchemy import extract, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import LabMember, Publication, Publishes
from app.schemas.publication import (
    AuthorshipCreate,
    PublicationAuthorResponse,
    PublicationCreate,
    PublicationDetailResponse,
    PublicationListResponse,
    PublicationUpdate,
)


def author_to_response(member: LabMember) -> PublicationAuthorResponse:
    member_type = (
        member.type.value if hasattr(member.type, "value") else str(member.type)
    )
    return PublicationAuthorResponse(
        mid=member.mid,
        name=member.name,
        type=member_type,
    )


def publication_to_list_response(
    publication: Publication,
) -> PublicationListResponse:
    return PublicationListResponse(
        pubid=publication.pubid,
        title=publication.title,
        venue=publication.venue,
        date=publication.date,
        doi=publication.doi,
        author_count=len(publication.publishes),
    )


def publication_to_detail_response(
    publication: Publication,
) -> PublicationDetailResponse:
    authors = [
        author_to_response(publish.member)
        for publish in publication.publishes
        if publish.member is not None
    ]
    authors.sort(key=lambda author: author.mid)

    return PublicationDetailResponse(
        pubid=publication.pubid,
        title=publication.title,
        venue=publication.venue,
        date=publication.date,
        doi=publication.doi,
        authors=authors,
    )


async def get_publication_model(
    db: AsyncSession,
    pubid: int,
) -> Publication | None:
    result = await db.execute(
        select(Publication)
        .options(selectinload(Publication.publishes).selectinload(Publishes.member))
        .where(Publication.pubid == pubid)
        .execution_options(populate_existing=True)
    )
    return result.scalar_one_or_none()


async def lab_member_exists(db: AsyncSession, mid: int) -> bool:
    result = await db.execute(select(LabMember.mid).where(LabMember.mid == mid))
    return result.scalar_one_or_none() is not None


async def authorship_exists(db: AsyncSession, pubid: int, mid: int) -> bool:
    result = await db.execute(
        select(Publishes).where(Publishes.pubid == pubid, Publishes.mid == mid)
    )
    return result.scalar_one_or_none() is not None


async def list_publications(
    db: AsyncSession,
    year: int | None = None,
    venue: str | None = None,
    author_mid: int | None = None,
) -> list[PublicationListResponse]:
    query = (
        select(Publication)
        .options(selectinload(Publication.publishes).selectinload(Publishes.member))
        .order_by(Publication.pubid)
    )

    if year is not None:
        query = query.where(extract("year", Publication.date) == year)
    if venue is not None:
        query = query.where(Publication.venue == venue)
    if author_mid is not None:
        query = query.join(Publishes).where(Publishes.mid == author_mid)

    result = await db.execute(query)
    publications = result.scalars().unique().all()
    return [publication_to_list_response(publication) for publication in publications]


async def get_publication(
    db: AsyncSession,
    pubid: int,
) -> PublicationDetailResponse | None:
    publication = await get_publication_model(db, pubid)
    if publication is None:
        return None
    return publication_to_detail_response(publication)


async def get_publication_authors(
    db: AsyncSession,
    pubid: int,
) -> list[PublicationAuthorResponse] | None:
    publication = await get_publication_model(db, pubid)
    if publication is None:
        return None
    return publication_to_detail_response(publication).authors


async def create_publication(
    db: AsyncSession,
    payload: PublicationCreate,
) -> PublicationDetailResponse:
    publication = Publication(**payload.model_dump())
    db.add(publication)

    try:
        await db.flush()
        created_pubid = publication.pubid
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    created = await get_publication_model(db, created_pubid)
    if created is None:
        raise RuntimeError("created publication could not be loaded")
    return publication_to_detail_response(created)


async def update_publication(
    db: AsyncSession,
    pubid: int,
    payload: PublicationUpdate,
) -> PublicationDetailResponse | None:
    publication = await get_publication_model(db, pubid)
    if publication is None:
        return None

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(publication, field, value)

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    updated = await get_publication_model(db, pubid)
    if updated is None:
        raise RuntimeError("updated publication could not be loaded")
    return publication_to_detail_response(updated)


async def delete_publication(db: AsyncSession, pubid: int) -> bool:
    publication = await get_publication_model(db, pubid)
    if publication is None:
        return False

    try:
        for publish in list(publication.publishes):
            await db.delete(publish)
        await db.delete(publication)
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    return True


async def add_publication_author(
    db: AsyncSession,
    pubid: int,
    payload: AuthorshipCreate,
) -> PublicationDetailResponse:
    publication = await get_publication_model(db, pubid)
    if publication is None:
        raise LookupError("publication not found")
    if not await lab_member_exists(db, payload.mid):
        raise LookupError("lab member not found")
    if await authorship_exists(db, pubid, payload.mid):
        raise ValueError("authorship already exists")

    db.add(Publishes(pubid=pubid, mid=payload.mid))

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    updated = await get_publication_model(db, pubid)
    if updated is None:
        raise RuntimeError("updated publication could not be loaded")
    return publication_to_detail_response(updated)


async def remove_publication_author(
    db: AsyncSession,
    pubid: int,
    mid: int,
) -> bool:
    if await get_publication_model(db, pubid) is None:
        raise LookupError("publication not found")

    result = await db.execute(
        select(Publishes).where(Publishes.pubid == pubid, Publishes.mid == mid)
    )
    authorship = result.scalar_one_or_none()
    if authorship is None:
        return False

    try:
        await db.delete(authorship)
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    return True
