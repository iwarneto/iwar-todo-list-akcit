# To-Do List API

Micro-API RESTful para gerenciamento de tarefas: criar, listar, atualizar, concluir e excluir tarefas, com filtro por status. Os dados ficam em um banco SQLite local.

Mini projeto da pós-graduação UFG / AKCIT, desenvolvido com o auxílio de IA generativa em todas as etapas, da arquitetura aos testes.

## Funcionalidades

- CRUD completo de tarefas (`/tasks`)
- Marcar tarefa como concluída (`status: done`)
- Filtrar a listagem por status (`pending` ou `done`)
- Validação dos dados de entrada, com respostas `422` claras
- Documentação interativa automática (Swagger UI) em `/docs`

## Tecnologias

| Item | Tecnologia |
|---|---|
| Linguagem | Python 3.12+ |
| Gerenciador de pacotes | [uv](https://docs.astral.sh/uv/) |
| Framework web | [FastAPI](https://fastapi.tiangolo.com/) + Uvicorn |
| ORM e validação | [SQLModel](https://sqlmodel.tiangolo.com/) (SQLAlchemy + Pydantic) |
| Banco de dados | SQLite |
| Testes | pytest + `TestClient` (httpx2) |
| Lint e formatação | Ruff |
| IA generativa | [Claude Code](https://claude.com/claude-code) (Anthropic), com o modelo **Claude Opus 5.5** |

## Como rodar localmente

### Opção 1 — com uv (recomendado)

```bash
git clone https://github.com/iwarneto/iwar-todo-list-akcit.git
cd iwar-todo-list-akcit
uv sync
uv run uvicorn app.main:app --reload
```

O `uv sync` cria o ambiente virtual e instala as versões exatas do `uv.lock`.

### Opção 2 — com pip

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Com o servidor no ar, acesse **http://127.0.0.1:8000/docs** para testar a API pelo navegador. O banco `todo.db` é criado automaticamente na primeira execução.

## Endpoints

| Método | Rota | Descrição | Sucesso |
|---|---|---|---|
| `POST` | `/tasks` | Cria uma tarefa | `201` |
| `GET` | `/tasks` | Lista as tarefas (`?status=pending` ou `?status=done`) | `200` |
| `GET` | `/tasks/{id}` | Busca uma tarefa | `200` |
| `PATCH` | `/tasks/{id}` | Atualiza os campos enviados | `200` |
| `DELETE` | `/tasks/{id}` | Exclui uma tarefa | `204` |

Uma tarefa inexistente retorna `404`, e dados inválidos retornam `422`.

## Exemplos de uso

> No Windows PowerShell, use `curl.exe` em vez de `curl`.

**Criar uma tarefa**

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Estudar FastAPI", "description": "Capítulo 2"}'
```

```json
{
  "title": "Estudar FastAPI",
  "description": "Capítulo 2",
  "id": 1,
  "status": "pending",
  "created_at": "2026-10-08T19:38:15.591110Z"
}
```

**Marcar como concluída**

```bash
curl -X PATCH http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

**Listar só as tarefas pendentes**

```bash
curl "http://127.0.0.1:8000/tasks?status=pending"
```

**Excluir**

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/1
```

## Testes

```bash
uv run pytest
```

São 22 testes: 5 unitários da camada de serviço e 17 dos endpoints. Eles usam um SQLite em memória, isolado a cada teste, e não alteram o `todo.db`.

Para checar o estilo do código:

```bash
uv run ruff check .
```

## Estrutura do projeto

```
app/
├── main.py          # aplicação FastAPI e tratamento de erros
├── routes.py        # endpoints (controller)
├── service.py       # regras de negócio
├── repository.py    # acesso ao banco
├── models.py        # tabela Task e schemas de entrada e saída
└── database.py      # conexão com o SQLite
tests/
├── conftest.py      # fixtures: banco em memória e cliente HTTP
├── test_service.py
└── test_api.py
docs/
└── arquitetura.md   # diagramas Mermaid e decisões de arquitetura
```

A arquitetura em camadas (controller → service → repository) e os diagramas estão em [docs/arquitetura.md](docs/arquitetura.md).

## Uso de IA generativa no desenvolvimento

O projeto foi construído em pareamento com o **Claude Code** (modelo **Claude Opus 5.5**), seguindo as etapas do material da disciplina. As decisões finais e a revisão ficaram com o autor.

| Etapa | Como a IA ajudou |
|---|---|
| Configuração do repositório | Geração do `.gitignore` e do `.gitattributes`, e criação do repositório no GitHub |
| Escolha de tecnologias | Comparação entre a stack do material e alternativas atuais (uv, SQLModel, Ruff), com foco em manter o projeto simples |
| Arquitetura | Diagramas de componentes e de sequência em Mermaid, e a estrutura de pastas |
| Dependências | Seleção enxuta dos pacotes, trocando `fastapi[standard]` (58 pacotes) por dependências explícitas (26 pacotes) |
| Código | Models, repository, service e endpoints |
| Testes | Fixtures com banco em memória e casos de sucesso e de erro |
| Commits | Mensagens no padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/) |
| Documentação | Este README |

## Limitações e próximos passos

**Limitações atuais**

- Sem autenticação: qualquer pessoa com acesso à API vê e altera todas as tarefas.
- SQLite em arquivo local, adequado para uso individual e não para muitos acessos simultâneos.
- Sem migrations: se o modelo mudar, é preciso apagar o `todo.db` para recriar a tabela.
- A listagem não tem paginação.

**Próximos passos possíveis**

- Frontend em React consumindo a API.
- Autenticação com JWT e tarefas por usuário.
- PostgreSQL com migrations via Alembic. Como o acesso ao banco está isolado no repository, a troca exige poucas mudanças.
- Paginação e ordenação na listagem, além de campos como prazo e prioridade.
- CI no GitHub Actions rodando testes e lint a cada push.

## Créditos e licença

Desenvolvido por **[iwarneto](https://github.com/iwarneto)** como mini projeto da pós-graduação UFG / AKCIT, a partir da sugestão "Micro-API de Gerenciamento de Tarefas (To-Do List)" do material da disciplina.

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE).
