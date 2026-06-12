from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_admin
from app.crud.publications import (
    add_publication_author,
    create_publication,
    delete_publication,
    get_publication,
    get_publication_authors,
    list_publications,
    remove_publication_author,
    update_publication,
)
from app.db import get_db
from app.schemas.publication import (
    AuthorshipCreate,
    DeleteResponse,
    PublicationAuthorResponse,
    PublicationCreate,
    PublicationDetailResponse,
    PublicationListResponse,
    PublicationUpdate,
)

router = APIRouter(tags=["publications"])


@router.get("/publications", response_model=list[PublicationListResponse])
async def read_publications(
    db: Annotated[AsyncSession, Depends(get_db)],
    year: int | None = None,
    venue: str | None = None,
    author_mid: int | None = None,
) -> list[PublicationListResponse]:
    return await list_publications(
        db,
        year=year,
        venue=venue,
        author_mid=author_mid,
    )


@router.get("/publications/{pubid}", response_model=PublicationDetailResponse)
async def read_publication(
    pubid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PublicationDetailResponse:
    publication = await get_publication(db, pubid)
    if publication is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="publication not found",
        )
    return publication


@router.get(
    "/publications/{pubid}/authors",
    response_model=list[PublicationAuthorResponse],
)
async def read_publication_authors(
    pubid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> list[PublicationAuthorResponse]:
    authors = await get_publication_authors(db, pubid)
    if authors is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="publication not found",
        )
    return authors


@router.post(
    "/publications",
    response_model=PublicationDetailResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
async def create_publication_endpoint(
    payload: PublicationCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PublicationDetailResponse:
    return await create_publication(db, payload)


@router.put(
    "/publications/{pubid}",
    response_model=PublicationDetailResponse,
    dependencies=[Depends(require_admin)],
)
async def update_publication_endpoint(
    pubid: int,
    payload: PublicationUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PublicationDetailResponse:
    publication = await update_publication(db, pubid, payload)
    if publication is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="publication not found",
        )
    return publication


@router.delete(
    "/publications/{pubid}",
    response_model=DeleteResponse,
    dependencies=[Depends(require_admin)],
)
async def delete_publication_endpoint(
    pubid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeleteResponse:
    deleted = await delete_publication(db, pubid)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="publication not found",
        )
    return DeleteResponse(message="publication deleted")


@router.post(
    "/publications/{pubid}/authors",
    response_model=PublicationDetailResponse,
    dependencies=[Depends(require_admin)],
)
async def add_publication_author_endpoint(
    pubid: int,
    payload: AuthorshipCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PublicationDetailResponse:
    try:
        return await add_publication_author(db, pubid, payload)
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.delete(
    "/publications/{pubid}/authors/{mid}",
    response_model=DeleteResponse,
    dependencies=[Depends(require_admin)],
)
async def remove_publication_author_endpoint(
    pubid: int,
    mid: int,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeleteResponse:
    try:
        deleted = await remove_publication_author(db, pubid, mid)
    except LookupError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="authorship not found",
        )
    return DeleteResponse(message="authorship deleted")
