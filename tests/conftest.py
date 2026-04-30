import asyncio
import os
from collections.abc import AsyncGenerator, Generator
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from alembic import command
from alembic.config import Config

os.environ.setdefault(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/lab_db",
)
os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]
os.environ["SECRET_KEY"] = "test-only-secret-key"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "60"
os.environ["ADMIN_USERNAME"] = "admin"

from app.core.security import create_access_token, get_password_hash  # noqa: E402

os.environ["ADMIN_PASSWORD_HASH"] = get_password_hash("admin123")

from app.db import get_db  # noqa: E402
from app.main import app  # noqa: E402

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_DATABASE_URL = os.environ["TEST_DATABASE_URL"]


APPLICATION_TABLES = [
    "publishes",
    '"uses"',
    "publication",
    "device",
    "equipment",
    '"grant"',
    "works",
    "project",
    "faculty",
    "collaborator",
    "student",
    "lab_member",
]


def run_alembic_upgrade() -> None:
    alembic_cfg = Config(str(PROJECT_ROOT / "alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")


async def reset_and_seed_database() -> None:
    engine = create_async_engine(TEST_DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    seed_sql = (PROJECT_ROOT / "seed" / "seed.sql").read_text(encoding="utf-8")
    statements = [statement.strip() for statement in seed_sql.split(";")]

    async with async_session() as session:
        table_list = ", ".join(APPLICATION_TABLES)
        await session.execute(
            text(f"TRUNCATE TABLE {table_list} RESTART IDENTITY CASCADE")
        )

        for statement in statements:
            if statement:
                await session.execute(text(statement))

        await session.commit()

    await engine.dispose()


@pytest.fixture(scope="session", autouse=True)
def setup_db() -> Generator[None, None]:
    run_alembic_upgrade()
    asyncio.run(reset_and_seed_database())
    yield


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    engine = create_async_engine(TEST_DATABASE_URL)

    async with engine.connect() as connection:
        transaction = await connection.begin()
        test_session = AsyncSession(bind=connection, expire_on_commit=False)

        async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
            yield test_session

        app.dependency_overrides[get_db] = override_get_db

        try:
            transport = ASGITransport(app=app)
            async with AsyncClient(
                transport=transport,
                base_url="http://test",
            ) as client:
                yield client
        finally:
            app.dependency_overrides.clear()
            await test_session.close()
            await transaction.rollback()

    await engine.dispose()


@pytest.fixture
async def admin_token(async_client: AsyncClient) -> str:
    response = await async_client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    return response.json()["access_token"]


@pytest.fixture
async def auth_headers(admin_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def viewer_token() -> str:
    return create_access_token(subject="viewer", role="viewer")


@pytest.fixture
def viewer_headers(viewer_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {viewer_token}"}
