from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_admin
from app.crud.seed import database_has_seed_data, run_seed_sql
from app.db import get_db
from app.schemas.admin import SeedResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post(
    "/seed",
    response_model=SeedResponse,
    dependencies=[Depends(require_admin)],
)
async def seed_database(db: Annotated[AsyncSession, Depends(get_db)]) -> SeedResponse:
    if await database_has_seed_data(db):
        return SeedResponse(message="already seeded", inserted=False)

    await run_seed_sql(db)
    return SeedResponse(message="seed data inserted", inserted=True)
