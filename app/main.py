import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting research-lab-manager API")
    yield
    logger.info("Shutting down research-lab-manager API")


app = FastAPI(title="Research Lab Manager", lifespan=lifespan)

# Routers will be registered here in later phases.


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "research-lab-manager"}
