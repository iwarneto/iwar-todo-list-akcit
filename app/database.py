from collections.abc import Iterator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./todo.db"

# check_same_thread=False: o FastAPI pode usar a conexão em threads diferentes.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Iterator[Session]:
    """Abre uma sessão por requisição e a fecha ao final."""
    with Session(engine) as session:
        yield session
