.PHONY: install run test lint format requirements

install:  ## Instala as dependências (inclui as de desenvolvimento)
	uv sync

run:  ## Inicia a API em http://127.0.0.1:8000 com recarga automática
	uv run uvicorn app.main:app --reload

test:  ## Executa os testes
	uv run pytest

lint:  ## Verifica estilo e formatação sem alterar arquivos
	uv run ruff check .
	uv run ruff format --check .

format:  ## Corrige o estilo e formata o código
	uv run ruff check --fix .
	uv run ruff format .

requirements:  ## Regenera o requirements.txt a partir do uv.lock
	uv export --no-hashes --no-header --no-annotate -o requirements.txt
