from pathlib import Path

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import LabMember


def get_seed_sql_path() -> Path:
    return Path(__file__).resolve().parents[2] / "seed" / "seed.sql"


async def database_has_seed_data(db: AsyncSession) -> bool:
    result = await db.execute(select(func.count()).select_from(LabMember))
    return result.scalar_one() > 0


async def run_seed_sql(db: AsyncSession) -> None:
    seed_sql = get_seed_sql_path().read_text(encoding="utf-8")
    statements = [statement.strip() for statement in seed_sql.split(";")]

    try:
        for statement in statements:
            if statement:
                await db.execute(text(statement))
        await db.commit()
    except Exception:
        await db.rollback()
        raise
