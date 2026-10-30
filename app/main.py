from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.api.routes.students import router as students_router
from app.db.base import Base
from app.db.session import engine
from app.models import student  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Create database tables when the application starts."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Student Management System",
    description="A simple backend API for managing student records.",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(students_router)
