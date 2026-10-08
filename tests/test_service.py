import pytest

from app.models import TaskCreate, TaskStatus, TaskUpdate
from app.repository import TaskRepository
from app.service import TaskNotFoundError, TaskService


@pytest.fixture
def service(session):
    return TaskService(TaskRepository(session))


def test_create_starts_as_pending(service):
    task = service.create(TaskCreate(title="Estudar"))

    assert task.id is not None
    assert task.status == TaskStatus.PENDING


def test_update_changes_only_sent_fields(service):
    task = service.create(TaskCreate(title="Estudar", description="cap. 2"))

    updated = service.update(task.id, TaskUpdate(status=TaskStatus.DONE))

    assert updated.status == TaskStatus.DONE
    assert updated.title == "Estudar"
    assert updated.description == "cap. 2"


def test_list_filters_by_status(service):
    service.create(TaskCreate(title="A"))
    done = service.create(TaskCreate(title="B"))
    service.update(done.id, TaskUpdate(status=TaskStatus.DONE))

    assert [t.title for t in service.list_tasks(TaskStatus.DONE)] == ["B"]
    assert [t.title for t in service.list_tasks(TaskStatus.PENDING)] == ["A"]
    assert len(service.list_tasks()) == 2


def test_get_missing_task_raises(service):
    with pytest.raises(TaskNotFoundError):
        service.get(999)


def test_delete_removes_task(service):
    task = service.create(TaskCreate(title="Apagar"))

    service.delete(task.id)

    with pytest.raises(TaskNotFoundError):
        service.get(task.id)
