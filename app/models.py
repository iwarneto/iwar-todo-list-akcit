from datetime import UTC, datetime
from enum import StrEnum

from pydantic import field_validator
from sqlmodel import Field, SQLModel


class TaskStatus(StrEnum):
    PENDING = "pending"
    DONE = "done"


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)


class Task(TaskBase, table=True):
    """Tabela `task` no banco de dados."""

    id: int | None = Field(default=None, primary_key=True)
    status: TaskStatus = Field(default=TaskStatus.PENDING, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class TaskCreate(TaskBase):
    """Dados aceitos na criação de uma tarefa."""


class TaskUpdate(SQLModel):
    """Atualização parcial: só os campos enviados são alterados."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    status: TaskStatus | None = None

    @field_validator("title", "status")
    @classmethod
    def reject_null(cls, value):
        # Omitir o campo é permitido; enviar `null` explicitamente não.
        if value is None:
            raise ValueError("não pode ser nulo")
        return value


class TaskRead(TaskBase):
    """Formato de resposta da API."""

    id: int
    status: TaskStatus
    created_at: datetime
