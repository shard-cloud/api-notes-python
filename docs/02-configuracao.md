## 🔐 Variáveis de Ambiente OBRIGATÓRIAS

**IMPORTANTE**: As variáveis marcadas como **(OBRIGATÓRIO)** são essenciais. A aplicação não funcionará sem elas.

### Arquivo `.env`

Copie `env.example` para `.env` e configure:

```env
# Database (OBRIGATÓRIO)
DATABASE=postgres://user:password@localhost:5432/notes_db

# Server (OBRIGATÓRIO)
PORT=80
HOST=0.0.0.0

# Security (OBRIGATÓRIO)
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Environment (OBRIGATÓRIO)
ENVIRONMENT=development
DEBUG=true
```

### Variáveis Detalhadas

#### `DATABASE` (obrigatório)

String de conexão PostgreSQL (suporta tanto `postgres://` quanto `postgresql://`):

```env
DATABASE=postgres://USER:PASSWORD@HOST:PORT/DATABASE
```

Exemplos:

```env
# Local
DATABASE=postgres://noteuser:notepass@localhost:5432/notes_db

# Docker Compose
DATABASE=postgres://noteuser:notepass@db:5432/notes_db

# Supabase
DATABASE=postgres://user:pass@db.xxx.supabase.co:5432/postgres

# Railway
DATABASE=postgres://user:pass@containers-us-west-1.railway.app:5432/railway

# Shard Cloud (com SSL)
DATABASE=postgres://user:pass@postgres.shardatabases.app:5432/database?ssl=true
```

#### `SECRET_KEY` (obrigatório em produção)

Chave secreta para assinar tokens JWT:

```bash
# Gerar chave segura
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

```env
SECRET_KEY=your-generated-secret-key-here
```

#### `ACCESS_TOKEN_EXPIRE_MINUTES` (opcional, padrão: 1440)

Tempo de expiração do token em minutos:

```env
ACCESS_TOKEN_EXPIRE_MINUTES=1440  # 24 horas
ACCESS_TOKEN_EXPIRE_MINUTES=60    # 1 hora
ACCESS_TOKEN_EXPIRE_MINUTES=10080 # 1 semana
```

## 🗄️ Configuração do Banco de Dados

### Opção 1: Docker Compose (Recomendado)

```bash
docker-compose up -d db
```

Credenciais padrão:
- **User:** noteuser
- **Password:** notepass
- **Database:** notes_db
- **Port:** 5432

### Opção 2: PostgreSQL Local

```bash
# Criar usuário e banco
psql -U postgres
CREATE USER noteuser WITH PASSWORD 'notepass';
CREATE DATABASE notes_db OWNER noteuser;
GRANT ALL PRIVILEGES ON DATABASE notes_db TO noteuser;
```

### Opção 3: PostgreSQL em Cloud

**Supabase (Grátis):**
1. Crie projeto em https://supabase.com
2. Vá em Settings > Database
3. Copie Connection String
4. Cole no `.env`

**Railway:**
1. Crie projeto em https://railway.app
2. Adicione PostgreSQL plugin
3. Copie `DATABASE_URL`

## 🔄 Migrations

### Configurar Alembic

```bash
# Inicializar (já feito)
alembic init alembic

# Criar migration
alembic revision --autogenerate -m "Initial migration"

# Aplicar migrations
alembic upgrade head

# Ver status
alembic current
alembic history
```

### Criar Nova Migration

```bash
# 1. Edite models em src/database.py
# 2. Gere migration
alembic revision --autogenerate -m "Add new field"

# 3. Revise o arquivo gerado
# 4. Aplique
alembic upgrade head
```

### Rollback

```bash
# Voltar uma migration
alembic downgrade -1

# Voltar para versão específica
alembic downgrade <revision_id>
```

## 🔐 Configuração de Segurança

### Sistema de Hash de Senhas

A API usa **PBKDF2** com SHA-256 para hash de senhas:

- **Salt**: Gerado automaticamente (16 bytes hex)
- **Iterações**: 100.000 rounds
- **Formato**: `salt:hash` (ex: `a1b2c3...:e4f5g6...`)

**Vantagens:**
- ✅ Mais seguro que bcrypt em alguns cenários
- ✅ Sem limitação de tamanho de senha
- ✅ Compatível com Python padrão (sem dependências extras)
- ✅ Resistente a ataques de força bruta

### JWT Secret Key

**Desenvolvimento:**
```env
SECRET_KEY=dev-secret-key-not-for-production
```

**Produção:**
```bash
# Gerar chave segura
openssl rand -hex 32
# ou
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### CORS (Cross-Origin Resource Sharing)

Editar `src/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://meuapp.com",
        "https://app.meuapp.com"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### Rate Limiting (Opcional)

```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/auth/token")
@limiter.limit("5/minute")
async def login(request: Request, ...):
    # ...
```

## 🌱 Seeds

### Criar Usuário Inicial

```bash
python seed/create_user.py
```

Isso cria usuário:
- **Username:** admin
- **Password:** admin123
- **Email:** admin@example.com

### Customizar Seed

Edite `seed/create_user.py`:

```python
admin_user = User(
    username="meuusuario",
    email="meu@email.com",
    hashed_password=get_password_hash("minhasenha123"),
    is_active=True
)
```

## 🐳 Docker

### Build Customizado

```bash
# Build da imagem
docker build -t api-notes-python .

# Run com variáveis
docker run -p 80:80 \
  -e DATABASE=postgresql://user:pass@host:5432/db \
  -e SECRET_KEY=your-secret-key \
  api-notes-python
```

### Docker Compose Personalizado

```yaml
version: '3.8'
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: ${DB_USER:-noteuser}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-notepass}
      POSTGRES_DB: ${DB_NAME:-notes_db}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  api:
    build: .
    environment:
      DATABASE: postgresql://${DB_USER:-noteuser}:${DB_PASSWORD:-notepass}@db:5432/${DB_NAME:-notes_db}
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      - db
```

## 🔧 Configuração Avançada

### Logs Estruturados

Editar `src/main.py`:

```python
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
```

### Connection Pool

Editar `src/database.py`:

```python
engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.debug,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)
```

### Cache (Redis - Opcional)

```bash
pip install redis aioredis
```

```python
import redis.asyncio as redis

redis_client = redis.from_url("redis://localhost:6379")

@app.get("/notes/")
async def get_notes(..., cache_key: str = None):
    if cache_key:
        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
    
    # ... lógica normal
    result = await get_notes_from_db()
    
    if cache_key:
        await redis_client.setex(cache_key, 300, json.dumps(result))
    
    return result
```

## 🎯 Próximos passos

Continue para [Rodando](./03-rodando.md) para executar e testar a API.
