from sqlmodel import Session, select

from app.models import Task, TaskStatus


class TaskRepository:
    """Único ponto de acesso ao banco de dados para tarefas."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def list_all(self, status: TaskStatus | None = None) -> list[Task]:
        query = select(Task).order_by(Task.id)
        if status is not None:
            query = query.where(Task.status == status)
        return list(self.session.exec(query).all())

    def get(self, task_id: int) -> Task | None:
        return self.session.get(Task, task_id)

    def save(self, task: Task) -> Task:
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.session.delete(task)
        self.session.commit()
