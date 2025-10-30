.PHONY: help dev build install migrate seed test lint format clean docker-up docker-down

help: ## Mostrar este help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

dev: ## Rodar em modo desenvolvimento
	uvicorn src.main:app --reload --host 0.0.0.0 --port 80

build: ## Instalar dependências
	pip install -r requirements.txt

install: ## Instalar dependências de desenvolvimento
	pip install -r requirements.txt
	pip install black ruff mypy pytest pytest-cov

migrate: ## Aplicar migrations
	alembic upgrade head

migrate-dev: ## Criar nova migration
	alembic revision --autogenerate -m "$(msg)"

seed: ## Criar usuário inicial
	python seed/create_user.py

test: ## Rodar testes
	pytest

test-cov: ## Rodar testes com coverage
	pytest --cov=src --cov-report=html

lint: ## Rodar linter
	ruff check src/ tests/
	black --check src/ tests/
	mypy src/

format: ## Formatar código
	black src/ tests/
	ruff check --fix src/ tests/

clean: ## Limpar cache e arquivos temporários
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

docker-up: ## Subir containers (banco + API)
	docker-compose up -d

docker-down: ## Parar containers
	docker-compose down

docker-logs: ## Ver logs dos containers
	docker-compose logs -f

.DEFAULT_GOAL := help
