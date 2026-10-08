import pytest

from app.models import DESCRIPTION_MAX_LENGTH, TITLE_MAX_LENGTH


def create_task(client, **data):
    response = client.post("/tasks", json={"title": "Estudar FastAPI", **data})
    assert response.status_code == 201
    return response.json()


def test_create_task(client):
    task = create_task(client, description="cap. 2")

    assert task["title"] == "Estudar FastAPI"
    assert task["description"] == "cap. 2"
    assert task["status"] == "pending"
    assert "id" in task and "created_at" in task


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"title": ""},
        {"title": "x" * (TITLE_MAX_LENGTH + 1)},
        {"title": "ok", "description": "x" * (DESCRIPTION_MAX_LENGTH + 1)},
    ],
)
def test_create_task_rejects_invalid_data(client, payload):
    assert client.post("/tasks", json=payload).status_code == 422


def test_create_task_accepts_max_lengths(client):
    task = create_task(
        client, title="x" * TITLE_MAX_LENGTH, description="x" * DESCRIPTION_MAX_LENGTH
    )

    assert len(task["title"]) == TITLE_MAX_LENGTH


def test_list_tasks(client):
    create_task(client, title="A")
    create_task(client, title="B")

    response = client.get("/tasks")

    assert response.status_code == 200
    assert [t["title"] for t in response.json()] == ["A", "B"]


def test_list_tasks_filtered_by_status(client):
    create_task(client, title="Pendente")
    done = create_task(client, title="Concluída")
    client.patch(f"/tasks/{done['id']}", json={"status": "done"})

    pending = client.get("/tasks", params={"status": "pending"}).json()
    finished = client.get("/tasks", params={"status": "done"}).json()

    assert [t["title"] for t in pending] == ["Pendente"]
    assert [t["title"] for t in finished] == ["Concluída"]


def test_list_tasks_rejects_unknown_status(client):
    assert client.get("/tasks", params={"status": "xyz"}).status_code == 422


def test_get_task(client):
    task = create_task(client)

    response = client.get(f"/tasks/{task['id']}")

    assert response.status_code == 200
    assert response.json() == task


def test_mark_task_as_done(client):
    task = create_task(client, description="cap. 2")

    response = client.patch(f"/tasks/{task['id']}", json={"status": "done"})

    assert response.status_code == 200
    assert response.json()["status"] == "done"
    assert response.json()["description"] == "cap. 2"


def test_update_can_clear_description(client):
    task = create_task(client, description="cap. 2")

    response = client.patch(f"/tasks/{task['id']}", json={"description": None})

    assert response.json()["description"] is None


@pytest.mark.parametrize("field", ["title", "status"])
def test_update_rejects_null_required_fields(client, field):
    task = create_task(client)

    assert client.patch(f"/tasks/{task['id']}", json={field: None}).status_code == 422


def test_delete_task(client):
    task = create_task(client)

    assert client.delete(f"/tasks/{task['id']}").status_code == 204
    assert client.get(f"/tasks/{task['id']}").status_code == 404


@pytest.mark.parametrize(
    ("method", "body"),
    [("get", None), ("patch", {"status": "done"}), ("delete", None)],
)
def test_missing_task_returns_404(client, method, body):
    kwargs = {"json": body} if body else {}

    response = client.request(method.upper(), "/tasks/999", **kwargs)

    assert response.status_code == 404
    assert response.json() == {"detail": "Tarefa 999 não encontrada"}


def test_root_redirects_to_docs(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/docs"
