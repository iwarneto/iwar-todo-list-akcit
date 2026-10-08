from app.models import Task, TaskCreate, TaskStatus, TaskUpdate
from app.repository import TaskRepository


class TaskNotFoundError(Exception):
    def __init__(self, task_id: int) -> None:
        super().__init__(f"Tarefa {task_id} não encontrada")
        self.task_id = task_id


class TaskService:
    """Regras de negócio das tarefas, sem conhecer HTTP nem SQL."""

    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def create(self, data: TaskCreate) -> Task:
        task = Task.model_validate(data)
        return self.repository.save(task)

    def list_tasks(self, status: TaskStatus | None = None) -> list[Task]:
        return self.repository.list_all(status)

    def get(self, task_id: int) -> Task:
        task = self.repository.get(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def update(self, task_id: int, data: TaskUpdate) -> Task:
        task = self.get(task_id)
        task.sqlmodel_update(data.model_dump(exclude_unset=True))
        return self.repository.save(task)

    def delete(self, task_id: int) -> None:
        self.repository.delete(self.get(task_id))
