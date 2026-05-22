"""
FastAPI application entry point.
"""
import asyncio
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from backend.api.content import router as content_router
from backend.api.export import router as export_router
from backend.api.generation import router as generation_router
from backend.api.questions import router as questions_router
from backend.config import settings
from backend.db.connection import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run schema.sql on startup if tables don't exist
    schema_path = Path(__file__).parent / "db" / "schema.sql"
    if schema_path.exists():
        async with engine.begin() as conn:
            await conn.execute(text(schema_path.read_text()))
    yield
    await engine.dispose()


app = FastAPI(
    title="Question Generation API",
    description="Agentic AI-powered English assessment question generation",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(content_router)
app.include_router(generation_router)
app.include_router(questions_router)
app.include_router(export_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "question-generation-api"}
