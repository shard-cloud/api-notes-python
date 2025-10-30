# API de Notas (Notes API)

API REST completa para gerenciamento de notas com FastAPI, SQLAlchemy, Alembic e autenticação por token. CRUD, busca, filtros e segurança.

## 🎯 Características

- ✅ CRUD completo de notas
- ✅ Autenticação JWT com hash PBKDF2
- ✅ Busca por título e conteúdo
- ✅ Filtros e paginação
- ✅ PostgreSQL + SQLAlchemy ORM
- ✅ Migrations com Alembic
- ✅ Validação com Pydantic
- ✅ Docker e Docker Compose
- ✅ Health check endpoint
- ✅ CORS configurado
- ✅ Logs estruturados

## 📋 Requisitos

- Python 3.11+
- PostgreSQL 14+ (ou use Docker Compose)
- Docker (opcional)

## 🚀 Como rodar

### Com Docker Compose (Recomendado)

```bash
# Copiar .env
cp .env.example .env

# Subir banco e aplicação
docker-compose up -d

# Rodar migrations
docker-compose exec api alembic upgrade head

# Criar usuário inicial
docker-compose exec api python seed/create_user.py

# Acesse: http://localhost:80/health
```

### Sem Docker

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis OBRIGATÓRIAS no .env
cp .env.example .env
# Editar .env com suas configurações de banco e segurança

# Rodar migrations
alembic upgrade head

# Criar usuário
python seed/create_user.py

# Iniciar servidor
python src/main.py
```

## 📦 Scripts

```bash
# Desenvolvimento
uvicorn src.main:app --reload

# Migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1

# Testes
pytest
pytest --cov=src

# Linting
black src/ tests/
ruff check src/ tests/
mypy src/
```

## 🔗 Endpoints

### Autenticação
```
POST /auth/token    # Obter token de acesso
```

### Notas (requer autenticação)
```
GET    /notes              # Listar todas
GET    /notes/:id          # Buscar por ID
POST   /notes              # Criar nova
PUT    /notes/:id          # Atualizar
DELETE /notes/:id          # Deletar
GET    /notes/search?q=    # Buscar por texto
```

### Exemplos

**Obter Token:**
```bash
curl -X POST http://localhost:80/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**Criar Nota:**
```bash
curl -X POST http://localhost:80/notes \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Minha nota","content":"Conteúdo"}'
```

## 📂 Estrutura

```
api-notes-python/
├── alembic/               # Migrations
├── src/
│   ├── main.py            # Entry point FastAPI
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── routes/            # Endpoints
│   ├── services/          # Lógica de negócio
│   ├── auth/              # Autenticação
│   └── database.py        # Configuração DB
├── seed/                  # Scripts de seed
├── tests/                 # Testes pytest
└── docs/                  # Documentação
```

## 🗄️ Banco de dados

### Modelo de Note

```python
class Note:
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user_id: int
```

### Conexão

```env
DATABASE=postgres://user:password@localhost:5432/notes_db
```

## 🔐 Autenticação

Sistema de autenticação JWT com hash PBKDF2:

1. POST `/auth/token` com username/password
2. Recebe token de acesso JWT
3. Usa token no header: `Authorization: Bearer TOKEN`
4. Token expira em 24 horas (configurável)
5. Senhas hasheadas com PBKDF2 + salt seguro

## 🐳 Docker

```bash
# Build
docker build -t api-notes-python .

# Run
docker run -p 80:80 \
  -e DATABASE=postgres://user:pass@host:5432/db \
  api-notes-python
```

## 📊 Swagger Docs

Documentação interativa disponível em:

- **Swagger UI:** http://localhost:80/docs
- **ReDoc:** http://localhost:80/redoc
- **OpenAPI JSON:** http://localhost:80/openapi.json

## 🧪 Testes

```bash
# Todos os testes
pytest

# Com coverage
pytest --cov=src --cov-report=html

# Testes específicos
pytest tests/test_notes.py
```

## 📄 Licença

MIT

---

