# Rodando o Projeto

## 🚀 Desenvolvimento Local

### Pré-requisitos

```bash
# Verificar versões
python --version  # 3.11+
pip --version     # 23+
docker --version  # 20+ (opcional)
```

### Setup Inicial

```bash
# 1. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar .env
cp env.example .env
# Edite .env com suas configurações

# 4. Rodar migrations
alembic upgrade head

# 5. Criar usuário inicial
python seed/create_user.py
```

### Iniciar Servidor

```bash
# Modo desenvolvimento (hot-reload)
python src/main.py

# Ou usar Makefile
make dev
```

Servidor rodando em **http://localhost:80**

### Logs Esperados

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Database tables created
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:80
```

**Nota:** Logs de debug do SQLAlchemy foram desabilitados para produção.

## 🐳 Com Docker Compose

### Subir Tudo

```bash
# Subir banco + API
docker-compose up -d

# Ver logs
docker-compose logs -f api

# Status
docker-compose ps
```

### Migrations e Seed (Docker)

```bash
# Aplicar migrations
docker-compose exec api alembic upgrade head

# Criar usuário
docker-compose exec api python seed/create_user.py

# Ver logs
docker-compose logs -f api
```

### Parar

```bash
# Parar containers
docker-compose down

# Parar e remover volumes
docker-compose down -v
```

## 🧪 Testando Endpoints

### Health Check

```bash
curl http://localhost:80/health

# Resposta esperada:
# {
#   "status": "ok",
#   "message": "API is healthy",
#   "version": "1.0.0"
# }
```

### Autenticação

**Registrar usuário:**
```bash
curl -X POST http://localhost:80/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

**Login (obter token):**
```bash
curl -X POST http://localhost:80/auth/token \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'

# Resposta:
# {
#   "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
#   "token_type": "bearer"
# }
```

### Notas (com autenticação)

**Criar nota:**
```bash
TOKEN="seu-token-aqui"

curl -X POST http://localhost:80/notes/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Minha primeira nota",
    "content": "Conteúdo da nota"
  }'
```

**Listar notas:**
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:80/notes/

# Com paginação
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:80/notes/?page=1&limit=5"

# Com busca
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:80/notes/?search=primeira"
```

**Buscar por ID:**
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:80/notes/1
```

**Atualizar nota:**
```bash
curl -X PUT http://localhost:80/notes/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Título atualizado",
    "content": "Conteúdo atualizado"
  }'
```

**Deletar nota:**
```bash
curl -X DELETE http://localhost:80/notes/1 \
  -H "Authorization: Bearer $TOKEN"
```

## 📊 Documentação Interativa

### Swagger UI

Acesse: **http://localhost:80/docs**

- Interface interativa
- Teste endpoints diretamente
- Documentação automática
- Schemas de request/response

### ReDoc

Acesse: **http://localhost:80/redoc**

- Documentação limpa e organizada
- Melhor para leitura
- Navegação por seções

### OpenAPI JSON

Acesse: **http://localhost:80/openapi.json**

- Schema OpenAPI 3.0
- Para integração com ferramentas
- Import em Postman/Insomnia

## 🧪 Testes Automatizados

### Rodar Todos os Testes

```bash
# Testes básicos
pytest

# Com coverage
pytest --cov=src --cov-report=html

# Verbose
pytest -v

# Testes específicos
pytest tests/test_auth.py
pytest tests/test_notes.py
```

### Testes Disponíveis

- ✅ Health check endpoint
- ✅ Registro de usuário
- ✅ Login e autenticação
- ✅ CRUD de notas
- ✅ Validação de dados
- ✅ Busca e paginação
- ✅ Proteção de rotas

### Output Esperado

```
========================= test session starts =========================
tests/test_auth.py::test_health_check PASSED
tests/test_auth.py::test_register_user PASSED
tests/test_auth.py::test_login_success PASSED
tests/test_notes.py::test_create_note PASSED
tests/test_notes.py::test_get_notes PASSED
tests/test_notes.py::test_update_note PASSED
tests/test_notes.py::test_delete_note PASSED
========================= 7 passed in 2.34s =========================
```

## 🔍 Debug e Troubleshooting

### Ver Queries SQL

Editar `.env`:

```env
DEBUG=true
```

Ou via código (`src/database.py`):

```python
engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    echo=True,  # Mostra queries SQL
)
```

### Verificar Conexão do Banco

```bash
# Testar conexão
python -c "
import asyncio
from src.database import engine
from sqlalchemy import text

async def test():
    async with engine.begin() as conn:
        result = await conn.execute(text('SELECT 1'))
        print('Database connected:', result.scalar())

asyncio.run(test())
"
```

### Verificar Migrations

```bash
# Status atual
alembic current

# Histórico
alembic history

# Ver migrations pendentes
alembic show head
```

### Logs Detalhados

```bash
# Desenvolvimento
python src/main.py --log-level debug

# Docker
docker-compose logs -f api
```

### Verificar Porta em Uso

```bash
# Linux/Mac
lsof -i :80

# Windows
netstat -ano | findstr :80
```

## 📈 Performance Testing

### Simples (cURL)

```bash
# Medir latência
time curl -H "Authorization: Bearer $TOKEN" http://localhost:80/notes/
```

### com Apache Bench

```bash
# 1000 requests, 10 concurrent
ab -n 1000 -c 10 -H "Authorization: Bearer $TOKEN" http://localhost:80/notes/
```

### com Artillery

```bash
npm install -g artillery

# Criar config.yml
artillery quick --count 100 --num 10 http://localhost:80/health

# Resultados esperados:
# - p95 latency: < 100ms
# - Requests/sec: > 500
```

## 🔄 Hot Reload

O servidor usa `--reload` do Uvicorn:

- Alterações em `src/**/*.py` recarregam automaticamente
- Não precisa reiniciar manualmente
- Logs mostram "Reloading..."

## 🎯 Checklist de Validação

Antes de considerar pronto:

- [ ] `pip install -r requirements.txt` sem erros
- [ ] `alembic upgrade head` aplica migrations
- [ ] `python seed/create_user.py` cria usuário
- [ ] `python src/main.py` inicia servidor
- [ ] `curl /health` retorna status ok
- [ ] `curl /auth/token` retorna token
- [ ] `curl /notes/` com token retorna lista
- [ ] `pytest` passa todos os testes
- [ ] `/docs` abre documentação Swagger
- [ ] Docker Compose sobe corretamente
- [ ] Logs estruturados aparecem

## 🚀 Próximos passos

Continue para [Deploy](./04-deploy.md) para colocar em produção.
