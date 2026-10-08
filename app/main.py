from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse

from app.database import create_db_and_tables
from app.routes import router
from app.service import TaskNotFoundError


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="To-Do List API",
    description="Micro-API de gerenciamento de tarefas — Mini Projeto AKCIT/UFG",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(router)


@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse("/docs")
