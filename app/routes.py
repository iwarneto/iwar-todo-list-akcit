from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.models import Task, TaskCreate, TaskRead, TaskStatus, TaskUpdate
from app.repository import TaskRepository
from app.service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service(session: Annotated[Session, Depends(get_session)]) -> TaskService:
    return TaskService(TaskRepository(session))


ServiceDep = Annotated[TaskService, Depends(get_task_service)]


@router.post("", response_model=TaskRead, status_code=201)
def create_task(data: TaskCreate, service: ServiceDep) -> Task:
    return service.create(data)


@router.get("", response_model=list[TaskRead])
def list_tasks(service: ServiceDep, status: TaskStatus | None = None) -> list[Task]:
    """Lista as tarefas. Use `?status=pending` ou `?status=done` para filtrar."""
    return service.list_tasks(status)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, service: ServiceDep) -> Task:
    return service.get(task_id)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, data: TaskUpdate, service: ServiceDep) -> Task:
    """Atualiza os campos enviados. Envie `{"status": "done"}` para concluir a tarefa."""
    return service.update(task_id, data)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, service: ServiceDep) -> None:
    service.delete(task_id)
